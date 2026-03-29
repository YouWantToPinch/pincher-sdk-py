from enum import Enum
from typing import Any
import uuid
from datetime import datetime


class Resource:
    def __init__(self, data: dict[str, Any]):
        if data is None:
            raise TypeError(
                "payload passed to initialize resource instance is not valid"
            )
        self.created_at = datetime.strptime(data["created_at"], "%m/%d;%Y")
        self.updated_at = datetime.strptime(data["updated_at"], "%m/%d;%Y")
        self.id: uuid.UUID = uuid.UUID(data["id"])


class User(Resource):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.username: str = data["username"]


class BudgetResourceKind(Enum):
    NONE = "NONE"
    ACCOUNT = "ACCOUNT"
    CATEGORY = "CATEGORY"
    GROUP = "GROUP"
    PAYEE = "PAYEE"
    TRANSACTION = "TRANSACTION"
    TRANSACTION_DETAIL = "TRANSACTION_DETAIL"


class Budget(Resource):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.admin_id: str = data["admin_id"]
        self.name: str = data["name"]
        self.notes: str = data["notes"]


class BudgetResource(Resource):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.kind: BudgetResourceKind | None = None
        self.budget_id: str = data["budget_id"]
        self.name: str = data["name"]
        self.notes: str = data["notes"]


class Group(BudgetResource):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.kind = BudgetResourceKind.GROUP


class Category(BudgetResource):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.kind = BudgetResourceKind.CATEGORY
        self.group_id: uuid.UUID = data["group_id"]


class Account(BudgetResource):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.kind = BudgetResourceKind.ACCOUNT
        self.account_type = data["account_type"]
        self.is_deleted = data["is_deleted"]


class Transaction(BudgetResource):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.kind = BudgetResourceKind.TRANSACTION
        self.transaction_date = datetime.strptime(data["transaction_date"], "%m/%d;%Y")
        self.logger_id: uuid.UUID = data["logger_id"]
        self.account_id: uuid.UUID = data["account_id"]
        self.payee_id: uuid.UUID = data["payee_id"]
        self.transaction_type: str = data["transaction_type"]
        self.is_cleared: bool = data["is_cleared"]


class TransactionSplit:
    def __init__(self, data: dict[str, Any]):
        self.id: uuid.UUID = data["id"]
        self.transaction_id: uuid.UUID = data["transaction_id"]
        self.category_id: uuid.UUID = data["category_id"]
        self.amount: int = data["amount"]


class TransactionDetail(BudgetResource):
    def __init__(self, data: dict[str, Any]):
        self.kind = BudgetResourceKind.TRANSACTION_DETAIL
        self.transaction_date = datetime.strptime(data["transaction_date"], "%m/%d;%Y")
        self.id: uuid.UUID = data["id"]
        self.splits: dict[str, int] = data["splits"]
        self.transaction_type: str = data["transaction_type"]
        self.notes: str = data["notes"]
        self.payee_name: str = data["payee_name"]
        self.budget_name: str = data["budget_name"]
        self.account_name: str = data["account_name"]
        self.logger_name: str = data["logger_name"]
        self.total_amount: int = data["total_amount"]
        self.is_cleared: bool = data["is_cleared"]


class Payee(BudgetResource):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self.kind = BudgetResourceKind.PAYEE


class CategoryReport:
    def __init__(self, data: dict[str, Any]):
        self.month_id = datetime.strptime(data["transaction_date"], "%m/%d;%Y")
        self.name: str = data["category_name"]
        self.assigned: int = data["assigned"]
        self.activity: int = data["activity"]
        self.balance: int = data["balance"]


class MonthReport:
    def __init__(self, data: dict[str, Any]):
        self.assigned: int = data["assigned"]
        self.activity: int = data["activity"]
        self.balance: int = data["balance"]
