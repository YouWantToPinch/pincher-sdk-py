from .types import Resource, Budget, BudgetResourceKind, BudgetResource
from collections import OrderedDict
import time
from threading import Lock


class ResourceCacheEntry:
    def __init__(
        self,
        data: Resource,
        destination_url: str,
        protected: bool = False,
    ) -> None:
        self.data: Resource = data
        self.destination_url: str = destination_url
        self.created_at = time.time()
        self.protected = protected


type ResourceCache = OrderedDict[str, ResourceCacheEntry]


class BudgetCache:
    def __init__(self, budget: ResourceCacheEntry) -> None:
        self.entry: ResourceCacheEntry = budget

        self.account_cache: ResourceCache = OrderedDict()
        self.payee_cache: ResourceCache = OrderedDict()
        self.group_cache: ResourceCache = OrderedDict()
        self.category_cache: ResourceCache = OrderedDict()
        self.txn_cache: ResourceCache = OrderedDict()
        self.txn_details_cache: ResourceCache = OrderedDict()

    def get_subcache(self, cache: BudgetResourceKind) -> ResourceCache | None:
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
    def __init__(self, capacity: int = 100, ttl_seconds: int = 60 * 5):
        self.entries: OrderedDict[str, BudgetCache] = OrderedDict()
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

            budget_cache = self.entries[budget_id]

            # Check if expired
            if time.time() > budget_cache.entry.created_at + self.ttl:
                del self.entries[budget_id]
                return None

            # Refresh position (LRU logic)
            self.entries.move_to_end(budget_id)
            if not resource_id or resource_kind is BudgetResourceKind.NONE:
                return budget_cache.entry.data
            if not resource_id:
                return None
            subcache = budget_cache.get_subcache(resource_kind)
            if subcache is None:
                return
            entry = subcache[resource_id]
            if time.time() > entry.created_at + self.ttl:
                del subcache[resource_id]
                return None
            return entry.data

    def set(
        self,
        entry: ResourceCacheEntry,
        budget_id: str = "",
    ) -> None:
        if isinstance(entry, Budget):
            with self.lock:
                if str(entry.id) in self.entries:
                    self.entries.move_to_end(str(entry.id))
                self.entries[str(entry.id)] = BudgetCache(entry)

                if len(self.entries) > self.capacity:
                    self.entries.popitem(last=False)
        elif not budget_id:
            return None
        elif isinstance(entry, BudgetResource):
            with self.lock:
                if str(budget_id) not in self.entries:
                    return None

                self.entries.move_to_end(budget_id)

                budget_cache = self.entries[budget_id]
                if (
                    not isinstance(entry.data, BudgetResource)
                    or entry.data.kind is None
                ):
                    return
                subcache = budget_cache.get_subcache(entry.data.kind)
                if subcache is None:
                    return

                subcache[(str(entry.data.id))] = entry

                if len(subcache) > self.capacity:
                    self.entries.popitem(last=False)

                if len(self.entries) > self.capacity:
                    self.entries.popitem(last=False)

    def delete(
        self,
        budget_id,
        resource_id: str = "",
        resource_kind: BudgetResourceKind = BudgetResourceKind.NONE,
    ):
        try:
            if budget_id not in self.entries:
                return
            if not resource_id and resource_kind is BudgetResourceKind.NONE:
                # only assume budget cache deletion if neither resource
                # parameter is supplied an argument (having only one
                # signifies unclear intensions and therefore warrants an error)
                self.entries.pop(resource_id)
                return
            if resource_id and resource_kind is not BudgetResourceKind.NONE:
                budget_cache = self.entries[budget_id]
                subcache = budget_cache.get_subcache(resource_kind)
                if subcache is None:
                    return
                subcache.pop(resource_id)
            else:
                if resource_id:
                    raise ValueError("Cache.delete: resource id provided without kind")
                raise ValueError("Cache.delete: resource kind provided without id")
        except ValueError as e:
            raise e
