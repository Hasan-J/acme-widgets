import re
from typing import Callable, DefaultDict, Dict, Iterable
from collections import defaultdict
from abc import ABC, abstractmethod

##############
# Widget Class
##############


class Widget:
    """Class representing the widget product.

    Args:
        description (str): Brief user description.
        code (str): Identifier for the widget.
        price (float): Price in usd.
    """

    def __init__(self, description: str, code: str, price: float) -> None:
        self.description = description
        self.code = code
        self.price = price


#########
# Catalog
#########


class WidgetCatalog:
    def __init__(self, widgets: Iterable[Widget]) -> None:
        """Widget catalog the provides a simple interface for managing
        and inspecting its widget contents.

        Args:
            widgets (Iterable[Widget]): Collection of widgets to initialize it with.
        """

        self.widgets = self.populate_catalog(widgets)

    def populate_catalog(self, widgets: Iterable[Widget]) -> Dict[str, Widget]:
        return_widgets = {}
        for widget in widgets:
            return_widgets[widget.code] = widget
        return return_widgets

    def get(self, code: str) -> Widget:
        if self.contains(code):
            return self.widgets[code]
        raise ValueError(f"Catalog does not contain widget with code {code}")

    def contains(self, code: str) -> bool:
        return code in self.widgets

    def __repr__(self) -> str:
        widgets_str_list = [
            f"- {w.description}, price ${w.price}, order with code {w.code}"
            for w in self.widgets.values()
        ]
        return "\n".join(widgets_str_list)


######################
# Delivery charge rule
######################


def delivery_charge(total: float) -> float | int:
    match total:
        case _ if total < 0:
            raise ValueError(f"'total' can't be a negative number {total}")
        case _ if total == 0:
            return 0
        case _ if total < 50:
            return 4.95
        case _ if total < 90:
            return 2.95
        case _:
            return 0


################
# Special Offers
################


class ISpecialOffer(ABC):
    """An interface for special offers. Implement this class to define
    discount logic, given a specific Basket instance.
    """

    # Brief description of how the offer works.
    # Define this value in implementations.
    description = None

    def __init__(self):
        if self.description is None:
            raise AttributeError("Class attribute 'description' cannot be None.")

    @abstractmethod
    def apply(self, basket: "Basket") -> float:
        """Imlpement offer logic, return total discount based on basket items & catalog."""
        ...


class RedWidgetCoolSpecialOffer(ISpecialOffer):
    """Special offer that provides discounts on red widgets.
    Whenever you buy one red widget you get the second for hald the price.
    """

    description = "Buy one red widget, get the second half price"

    def apply(self, basket: "Basket") -> float:
        red_widget_code = "R01"
        discount_on_red_widgets = (basket.items_ordered[red_widget_code] // 2) * (
            basket.catalog.get(red_widget_code).price / 2
        )

        return discount_on_red_widgets


class SpecialOfferHandler:
    def __init__(self, offers: Iterable[ISpecialOffer]):
        """Manages a collection of ISpecialOffer implementations and applies them on the
        current ordered items of a Basket in order to calculate the total discount amount.

        Args:
            offers (Iterable[ISpecialOffer]): Collection of special offers.
        """

        self.offers = offers

    def get_discount(self, basket: "Basket") -> float | int:
        total_discount = 0
        if len(basket.items_ordered):
            for offer in self.offers:
                total_discount += offer.apply(basket)
        return total_discount

    @property
    def available_offers(self):
        base_msg = "🔥 Offers available 🔥"
        return base_msg + "\n" + "\n".join([offer.description for offer in self.offers])


########
# Basket
########


class Basket:
    """Acts as the interface for viewing a wide collection of widgets, ordering new
    widgets and checking the total order amount.

    Args:
        catalog (WidgetCatalog): Pre-populated catalog.
        calculate_delivery_charge (Callable[[float], float]): A function that should accept
            a float as the only arg and return a float number representing the delivery charge.
        special_offers_handler (SpecialOfferHandler, optional): Initialized handler with a collection
            of special offers that should be provided for users of the basket. Defaults to None.
    """

    def __init__(
        self,
        catalog: WidgetCatalog,
        calculate_delivery_charge: Callable[[float], float],
        special_offers_handler: SpecialOfferHandler = None,
    ) -> None:

        self.catalog = catalog
        self.calculate_delivery_charge = calculate_delivery_charge
        self.special_offers_handler = special_offers_handler

        self.items_ordered: DefaultDict[str, int] = defaultdict(lambda: 0)

    def add(self, widget_code: str) -> None:
        """Add new widget to the basket."""
        if self.catalog.contains(widget_code):
            self.items_ordered[widget_code] += 1
        else:
            raise ValueError(f"Widget with code {widget_code} not found in catalog.")

    def total(self) -> float:
        """Get total basket price including delivery charge and special offers."""
        total = 0
        for widget_code, widget_count in self.items_ordered.items():
            total += self.catalog.get(widget_code).price * widget_count
        if self.special_offers_handler:
            total -= self.special_offers_handler.get_discount(self)
        total += self.calculate_delivery_charge(total)
        return total

    def clear(self) -> None:
        """Reset the basket as if it's new."""
        self.items_ordered = defaultdict(lambda: 0)

    @property
    def widgets(self) -> str:
        """
        Returns:
            str: Description of current widgets in the basket.
        """
        if len(self.items_ordered):
            current_widgets = "\n".join(
                [
                    f"{self.catalog.get(code).description}: {count}"
                    for code, count in self.items_ordered.items()
                ]
            )
            return current_widgets
        return "[]"

    @property
    def available_offers(self):
        """Get list of offers available in this basket."""
        if self.special_offers_handler:
            return self.special_offers_handler.available_offers
        else:
            return "Sad, no offers available this time."


def get_basket():
    """Utility function to bootstrap everything needed to use the Basket interface.

    Returns:
        Basket: basket instance.
    """

    widget_catalog = WidgetCatalog(
        widgets=[
            Widget(description="Red Widget", code="R01", price=32.95),
            Widget(description="Green Widget", code="G01", price=24.95),
            Widget(description="Blue Widget", code="B01", price=7.95),
        ]
    )

    basket = Basket(
        catalog=widget_catalog,
        calculate_delivery_charge=delivery_charge,
        special_offers_handler=SpecialOfferHandler(
            offers=[RedWidgetCoolSpecialOffer()]
        ),
    )

    return basket


def interactive_session():
    print("Welcome to the interactive session")
    print("✨ Your basket awaits your orders ✨")

    command = ""
    basket = get_basket()

    help_message = """Waiting for user prompt to be:
    - add code - Add new widget to the basket, code should be one of [R01, B01, G01]
    - total - Returns total price of the basket
    - widgets - Returns current widgets added to the basket
    - catalog - Returns details about the widget catalog 
    - offers - Returns current offers available
    - clear - Resets the basket
    - exit - exit this interactive session
    """

    print(help_message)

    while command != "exit":
        command = input("> ")

        match command:
            case _ if command.startswith("add"):
                match = re.match(pattern=r"add (\w+)", string=command)
                if match:
                    try:
                        basket.add(match.group(1))
                    except ValueError as err:
                        print(f"Encountered error while adding widget: {err}")
                else:
                    print("Unrecognized 'add' command")
            case "total":
                print(f"{basket.total():.3f}"[:-1])
            case "widgets":
                print("📦️ Current widgets 📦️")
                print(basket.widgets)
            case "catalog":
                print(basket.catalog)
            case "offers":
                print(basket.available_offers)
            case "clear":
                basket.clear()
            case "help":
                print(help_message)
            case "exit":
                break
            case _:
                print("Unknown input")


if __name__ == "__main__":
    interactive_session()
