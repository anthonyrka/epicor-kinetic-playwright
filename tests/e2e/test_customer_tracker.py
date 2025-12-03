import re
from playwright.sync_api import expect
from kinetic_playwright.fixtures import epicor_page


CUSTOMER_ID = "XYZ"


def test_customer_tracker_filter_and_open_detail(epicor_page):
    """
    Flow:

    1. Start from an authenticated Epicor page (epicor_page fixture).
       - If we're not already on CRMN9000 Customer Tracker grid, click the tile.
    2. Ensure the Customer Tracker grid is visible.
    3. Click the filter icon, type CUSTOMER_ID value into the 'Cust. ID Filter' textbox.
    4. Wait for the grid to show exactly one row with CustID equal to CUSTOMER_ID.
    5. Click the CUSTOMER_ID link in that row.
    6. Assert the detail view for CustID=CUSTOMER_ID is rendered (key field input).
    """
    page = epicor_page

    #
    # 1) Ensure we're on the Customer Tracker grid (CRMN9000, pageId=CustomerEntryForm)
    #
    if "CRMN9000" not in page.url or "pageId=CustomerEntryForm" not in page.url:
        # We're likely on /#/home or some other view → use the tile to get to CRMN9000.
        customer_tracker_tile = page.locator(".khp-tile", has_text="Customer Tracker").first
        expect(customer_tracker_tile).to_be_visible(timeout=30_000)
        customer_tracker_tile.click()

        # For SPA routing, just poll the URL with a regex.
        expect(page).to_have_url(
            re.compile(r".*CRMN9000.*pageId=CustomerEntryForm.*"),
            timeout=60_000,
        )

    #
    # 2) Wait for the grid/filter UI to be present
    #
    filter_icon = page.locator("span.mdi.mdi-filter").first
    expect(filter_icon).to_be_visible(timeout=60_000)
    filter_icon.click()

    #
    # 3) Type the value of CUSTOMER_ID into the 'Cust. ID Filter' textbox
    #
    cust_id_filter = page.locator("input[aria-label='Cust. ID Filter']").first
    expect(cust_id_filter).to_be_visible(timeout=60_000)

    cust_id_filter.click()
    cust_id_filter.fill(CUSTOMER_ID)
    cust_id_filter.press("Enter")  # explicit apply

    #
    # 4) WAIT for the grid row with that ID
    #
    body_rows = page.locator("tbody.k-table-tbody tr")
    matching_rows = body_rows.filter(has_text=CUSTOMER_ID)

    # Wait until the filter has produced exactly one matching row.
    expect(matching_rows).to_have_count(1, timeout=60_000)

    row = matching_rows.first

    # Inside that row, find the link with the customer ID.
    customer_link = row.locator("a", has_text=CUSTOMER_ID)
    expect(customer_link).to_be_visible(timeout=10_000)
    customer_link.click()

    #
    # 5) FINAL ASSERTION — stop when the key field input is rendered with the right value
    #
    key_field = page.locator("input#txtKeyField").first
    expect(key_field).to_be_visible(timeout=60_000)
    expect(key_field).to_have_value(CUSTOMER_ID, timeout=60_000)
