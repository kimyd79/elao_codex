import { test, expect, type Page } from '@playwright/test'

async function fixtureLogin(page: Page) {
  await page
    .getByRole('button')
    .filter({ hasText: /fixture/i })
    .click()
}

test('login gate and fixture login', async ({ page }) => {
  await page.goto('/initialization')
  await expect(page).toHaveURL(/\/login$/)
  await fixtureLogin(page)
  await expect(page).toHaveURL(/\/initialization$/)
  await expect(page.getByRole('heading', { name: 'Initialization' })).toBeVisible()
})

test('core React routes remain reachable after authentication', async ({ page }) => {
  await page.goto('/login')
  await fixtureLogin(page)
  for (const route of ['/lookup', '/analysis', '/project', '/logformat', '/metrics']) {
    await page.goto(route)
    await expect(page).not.toHaveURL(/\/login$/)
  }
})
