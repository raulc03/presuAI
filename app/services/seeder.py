from sqlmodel import Session, select

from app.schemas.type import TypeEnum
from app.models.category import Category


def seed_default_categories(session: Session):
    expense_names = [
        "Supermarkets and Groceries",
        "Home",
        "Utilities",
        "Transport and Car",
        "Medical and Health",
        "Food and Drinks",
        "Entertainment",
        "Shopping",
        "Beauty and Personal Care",
        "Sports and Fitness",
        "Education",
        "Travel and Holidays",
        "Pets",
        "Debt Payments",
        "Transfers and Withdrawals",
        "Savings and Investments",
        "Financial Expenses",
        "Gifts and Donations",
        "Own Business",
        "Others",
    ]

    income_names = [
        "Savings",
        "Salary",
        "Bonus",
        "Interests",
        "Others",
        "Collections",
    ]

    def category_exists(name: str, type_: TypeEnum) -> bool:
        stmt = select(Category).where(Category.name == name, Category.type == type_)
        return session.exec(stmt).first() is not None

    new_categories = []

    for name in expense_names:
        if not category_exists(name, TypeEnum.expense):
            new_categories.append(Category(name=name, type=TypeEnum.expense))

    for name in income_names:
        if not category_exists(name, TypeEnum.income):
            new_categories.append(Category(name=name, type=TypeEnum.income))

    if new_categories:
        session.add_all(new_categories)
        session.commit()
