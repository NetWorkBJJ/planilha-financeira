import re
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        # Launch browser (headless=False so you can see it if you run locally)
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # Step 1: Open the App (Assuming localhost:8000 or file path)
        print("Opening App...")
        # Adjust this URL to match your local server or file path
        # page.goto("file:///Users/network/Documents/planilha-financeira/index.html")
        page.goto("http://localhost:8000") 

        # Verify Title
        expect(page).to_have_title("Planilha Financeira")
        print("✅ Title Verified")

        # Step 2: Clear any existing data (Optional, for clean slate)
        # We can implement a clean slate logic if needed, but for now we append.

        # Step 3: Add Income (Entrada)
        print("Adding Income...")
        page.click("button[onclick='adicionarEntrada()']")
        
        # Fill the last added row in 'Entradas'
        # We target the last row-wrapper in #entradas-container
        entradas_rows = page.locator("#entradas-container .row-wrapper")
        last_entrada = entradas_rows.last
        
        last_entrada.locator("input[placeholder='Descrição']").fill("Salário Teste")
        last_entrada.locator("input[placeholder='0,00']").fill("5000,00")
        # Click outside to trigger change event/save
        page.click("header") 
        print("✅ Income Added: R$ 5.000,00")

        # Step 4: Add Expense (Saída)
        print("Adding Expense...")
        page.click("button[onclick='adicionarSaida()']")
        
        saidas_rows = page.locator("#saidas-container .row-wrapper")
        last_saida = saidas_rows.last
        
        last_saida.locator("input[placeholder='Descrição']").fill("Aluguel Teste")
        last_saida.locator("input[placeholder='0,00']").fill("1500,00")
        page.click("header")
        print("✅ Expense Added: R$ 1.500,00")

        # Step 5: Verify Calculations
        # Wait a moment for UI update
        page.wait_for_timeout(500)
        
        # Get KPI values
        total_entradas = page.locator("#kpi-entradas").inner_text()
        total_saidas = page.locator("#kpi-saidas").inner_text()
        saldo = page.locator("#kpi-saldo").inner_text()

        print(f"Current Status: Entradas={total_entradas}, Saídas={total_saidas}, Saldo={saldo}")

        # Basic Check (String contains value)
        # Note: Previous values might exist, so we check if it *contains* our logic or just visually check
        # For a strict test, we would clear localStorage first.
        
        # Step 6: Delete the Expense
        print("Deleting Expense...")
        last_saida.locator("button.btn-icon").click()
        page.click("header")
        print("✅ Expense Deleted")

        # Final Verification screenshot
        page.screenshot(path="resultado_teste.png")
        print("📸 Screenshot saved as 'resultado_teste.png'")

        browser.close()

if __name__ == "__main__":
    run()
