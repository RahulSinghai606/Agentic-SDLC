import { test, expect } from '@playwright/test';

test.describe('Listings and Payment Flow', () => {
  test('User can create, view, and delete listings', async ({ page }) => {
    await page.goto('/listings');
    await page.click('button#createListing');
    await page.fill('#title', 'Test Listing');
    await page.fill('#price', '100');
    await page.click('button[type=submit]');

    await expect(page.locator('.listing-title')).toHaveText('Test Listing');

    await page.click('button.delete-listing');
    await expect(page.locator('.listing-title')).not.toContainText('Test Listing');
  });

  test('User can complete payment for a listing', async ({ page }) => {
    await page.goto('/listings/1');
    await page.click('button#buyNow');
    await page.fill('#cardNumber', '4111111111111111');
    await page.fill('#expiryDate', '12/25');
    await page.fill('#cvv', '123');
    await page.click('button#pay');

    await expect(page.locator('.success')).toHaveText('Payment successful');
  });

  test('User sees error for failed payment', async ({ page }) => {
    await page.goto('/listings/1');
    await page.click('button#buyNow');
    await page.fill('#cardNumber', '0000000000000000');
    await page.fill('#expiryDate', '12/25');
    await page.fill('#cvv', '123');
    await page.click('button#pay');

    await expect(page.locator('.error')).toHaveText('Payment failed');
  });
});