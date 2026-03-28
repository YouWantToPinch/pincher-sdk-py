from client.types import Budget, BudgetResourceKind, BudgetResource
from collections import OrderedDict
from datetime import datetime
from src.client.types import Resource
import time
from threading import Lock


class ResourceCacheEntry:
    def __init__(
        self,
        data: Resource,
        destination_url: str,
        created_at: datetime,
        protected: bool = False,
    ) -> None:
        self.data: Resource = data
        self.destination_url: str = destination_url
        self.created_at = created_at
        self.protected = protected


class BudgetCache:
    def __init__(self, budget: ResourceCacheEntry) -> None:
        self.entry: ResourceCacheEntry = budget

        self.account_cache: OrderedDict[str, tuple[ResourceCacheEntry, float]] = (
            OrderedDict()
        )
        self.payee_cache: OrderedDict[str, tuple[ResourceCacheEntry, float]] = (
            OrderedDict()
        )
        self.group_cache: OrderedDict[str, tuple[ResourceCacheEntry, float]] = (
            OrderedDict()
        )
        self.category_cache: OrderedDict[str, tuple[ResourceCacheEntry, float]] = (
            OrderedDict()
        )
        self.txn_cache: OrderedDict[str, tuple[ResourceCacheEntry, float]] = (
            OrderedDict()
        )
        self.txn_details_cache: OrderedDict[str, tuple[ResourceCacheEntry, float]] = (
            OrderedDict()
        )

    def get_subcache(
        self, cache: BudgetResourceKind
    ) -> OrderedDict[str, tuple[ResourceCacheEntry, float]] | None:
        match cache:
            case BudgetResourceKind.ACCOUNT:
                return self.account_cache
            case BudgetResourceKind.PAYEE:
                return self.payee_cache
            case BudgetResourceKind.GROUP:
                return self.group_cache
            case BudgetResourceKind.CATEGORY:
                return self.category_cache
            case BudgetResourceKind.TRANSACTION:
                return self.txn_cache
            case BudgetResourceKind.TRANSACTION_DETAIL:
                return self.txn_details_cache
            case _:
                return None


class Cache:
    def __init__(self, capacity: int, ttl_seconds: int):
        self.entries: OrderedDict[str, tuple[BudgetCache, float]] = OrderedDict()
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.lock = Lock()

    def get(
        self,
        budget_id: str,
        resource_id: str = "",
        resource_kind: BudgetResourceKind = BudgetResourceKind.NONE,
    ) -> Resource | None:
        with self.lock:
            if budget_id not in self.entries:
                return None

            budget_cache, budget_cache_exp_time = self.entries[budget_id]

            # Check if expired
            if time.time() > budget_cache_exp_time:
                del self.entries[budget_id]
                return None

            # Refresh position (LRU logic)
            self.entries.move_to_end(budget_id)
            if not resource_kind or resource_kind is BudgetResourceKind.NONE:
                return budget_cache.entry.data
            if not resource_id:
                return None
            subcache = budget_cache.get_subcache(resource_kind)
            if subcache is None:
                return
            entry, entry_exp_time = subcache[resource_id]
            if time.time() > entry_exp_time:
                del subcache[resource_id]
                return None
            return entry.data

    def set(
        self,
        entry: ResourceCacheEntry,
        budget_id: str = "",
    ) -> None:
        exp_time = time.time() + self.ttl
        if isinstance(entry, Budget):
            with self.lock:
                if str(entry.id) in self.entries:
                    self.entries.move_to_end(str(entry.id))
                self.entries[str(entry.id)] = (BudgetCache(entry), exp_time)

                if len(self.entries) > self.capacity:
                    self.entries.popitem(last=False)
        elif not budget_id:
            return None
        elif isinstance(entry, BudgetResource):
            with self.lock:
                if str(budget_id) not in self.entries:
                    return None

                self.entries.move_to_end(budget_id)

                budget_cache, budget_cache_exp_time = self.entries[budget_id]
                if (
                    not isinstance(entry.data, BudgetResource)
                    or entry.data.kind is None
                ):
                    return
                subcache = budget_cache.get_subcache(entry.data.kind)
                if subcache is None:
                    return

                subcache[(str(entry.data.id))] = (entry, exp_time)

                if len(subcache) > self.capacity:
                    self.entries.popitem(last=False)

                if len(self.entries) > self.capacity:
                    self.entries.popitem(last=False)
