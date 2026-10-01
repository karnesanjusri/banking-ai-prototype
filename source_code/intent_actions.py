"""
intent_actions.py

A simple lookup table that maps each of the 77 BANKING77 intents to a short,
human-readable "recommended action" a support agent could take next.

This is intentionally simple (a Python dict), matching the assignment's
"does not need to be production-ready" instruction. In a real system this
would likely live in a database or a config file the support team can edit
without touching code.
"""

RECOMMENDED_ACTIONS = {
    # Cards: getting, using, delivery
    "activate_my_card": "Walk the customer through card activation steps",
    "apple_pay_or_google_pay": "Check digital wallet (Apple/Google Pay) support for their card",
    "card_about_to_expire": "Confirm replacement card has been ordered",
    "card_acceptance": "Check where the card type is accepted",
    "card_arrival": "Check card delivery status",
    "card_delivery_estimate": "Provide estimated card delivery window",
    "card_linking": "Help link the card to the customer's account",
    "card_not_working": "Run card diagnostics / check for card block",
    "card_swallowed": "Log ATM card-retention case and arrange replacement",
    "contactless_not_working": "Check contactless limit and card settings",
    "disposable_card_limits": "Share disposable virtual card limits",
    "get_disposable_virtual_card": "Guide customer to create a disposable virtual card",
    "get_physical_card": "Start physical card order",
    "getting_spare_card": "Start spare card order",
    "getting_virtual_card": "Guide customer to create a virtual card",
    "order_physical_card": "Start physical card order",
    "supported_cards_and_currencies": "Share supported card networks and currencies",
    "virtual_card_not_working": "Run virtual card diagnostics",
    "visa_or_mastercard": "Confirm card network (Visa/Mastercard) options",

    # Security, PIN, lost items
    "change_pin": "Guide customer through PIN change process",
    "compromised_card": "Freeze card immediately and start fraud review",
    "lost_or_stolen_card": "Freeze card immediately and arrange replacement",
    "lost_or_stolen_phone": "Review linked mobile-payment access and secure account",
    "passcode_forgotten": "Start identity-verified passcode reset",
    "pin_blocked": "Unblock PIN after identity verification",

    # Card payments and charges
    "card_payment_fee_charged": "Review the card payment fee with the customer",
    "card_payment_not_recognised": "Open a transaction dispute for the card payment",
    "card_payment_wrong_exchange_rate": "Review exchange rate applied to the card payment",
    "declined_card_payment": "Check reason for card payment decline",
    "direct_debit_payment_not_recognised": "Open a transaction dispute for the direct debit",
    "extra_charge_on_statement": "Review statement for unexpected charges",
    "pending_card_payment": "Check status of the pending card payment",
    "reverted_card_payment?": "Explain why the card payment was reverted",
    "transaction_charged_twice": "Open a duplicate-charge investigation",

    # Transfers
    "balance_not_updated_after_bank_transfer": "Check transfer status and expected balance update time",
    "beneficiary_not_allowed": "Check why the beneficiary is restricted",
    "cancel_transfer": "Attempt to cancel the pending transfer",
    "declined_transfer": "Check reason for transfer decline",
    "failed_transfer": "Investigate failed transfer and retry if possible",
    "pending_transfer": "Check transfer status",
    "receiving_money": "Confirm details for receiving a transfer",
    "transfer_fee_charged": "Review the transfer fee with the customer",
    "transfer_into_account": "Confirm account details for an incoming transfer",
    "transfer_not_received_by_recipient": "Trace the transfer and confirm recipient details",
    "transfer_timing": "Share expected transfer processing time",

    # Cash withdrawals and ATMs
    "atm_support": "Share nearby / supported ATM information",
    "cash_withdrawal_charge": "Review ATM withdrawal fee with the customer",
    "cash_withdrawal_not_recognised": "Open a transaction dispute for the ATM withdrawal",
    "declined_cash_withdrawal": "Check reason for ATM withdrawal decline",
    "pending_cash_withdrawal": "Check status of the pending ATM withdrawal",
    "wrong_amount_of_cash_received": "Open a cash-discrepancy investigation",
    "wrong_exchange_rate_for_cash_withdrawal": "Review exchange rate applied to the ATM withdrawal",

    # Top-ups and deposits
    "automatic_top_up": "Review automatic top-up settings",
    "balance_not_updated_after_cheque_or_cash_deposit": "Check deposit status and expected balance update time",
    "pending_top_up": "Check status of the pending top-up",
    "top_up_by_bank_transfer_charge": "Review bank-transfer top-up fee with the customer",
    "top_up_by_card_charge": "Review card top-up fee with the customer",
    "top_up_by_cash_or_cheque": "Confirm cash/cheque top-up process",
    "top_up_failed": "Investigate failed top-up and suggest another method",
    "top_up_limits": "Share top-up limits for the account",
    "top_up_reverted": "Explain why the top-up was reverted",
    "topping_up_by_card": "Confirm card top-up process",
    "verify_top_up": "Confirm source of funds for the top-up",

    # Identity and account
    "age_limit": "Share minimum/maximum age requirements",
    "country_support": "Confirm country/region availability",
    "edit_personal_details": "Help customer update personal details",
    "terminate_account": "Start account closure process",
    "unable_to_verify_identity": "Review identity documents and retry verification",
    "verify_my_identity": "Guide customer through identity verification steps",
    "verify_source_of_funds": "Request source-of-funds documentation",
    "why_verify_identity": "Explain identity verification requirement",

    # Currency exchange
    "exchange_charge": "Review currency exchange fee with the customer",
    "exchange_rate": "Share current exchange rate information",
    "exchange_via_app": "Guide customer through in-app currency exchange",
    "fiat_currency_support": "Share supported currencies list",

    # Refunds
    "request_refund": "Start refund request process",
    "Refund_not_showing_up": "Check refund status and expected posting time",
}


def get_recommended_action(intent: str) -> str:
    """
    Return a recommended action for the given intent.
    Falls back to a generic, readable action built from the intent name
    itself if the intent isn't in the table above (kept simple on purpose).
    """
    if intent in RECOMMENDED_ACTIONS:
        return RECOMMENDED_ACTIONS[intent]
    # Fallback: turn "wrong_exchange_rate_for_cash_withdrawal" into
    # "Review wrong exchange rate for cash withdrawal with the customer"
    readable = intent.replace("_", " ").replace("?", "").strip()
    return f"Review '{readable}' with the customer"
