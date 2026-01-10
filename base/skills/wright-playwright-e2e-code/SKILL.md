---
name: wright-playwright-e2e-code
description: Playwright E2E テストコードを生成。test.step で日本語ステップ名を使用し、コメント禁止。E2E テスト作成・Playwright コード生成時に使用。
---

# Playwright E2E テスト

## test.step 区切り

- What を説明するコメントは削除: 論理的な区切りは `test.step("日本語", async () => { ... })` で表現
- Why（目的・意図・理由）を説明するコメントは残す
- 日本語ステップ名: 「何をして、何を確認するか」が分かる表現。体言止めより動作表現を優先
- 適切な粒度: ユーザー操作単位・UI 状態確認単位で区切る。入れ子も可
- expect は step 内に含める
- 既に step に分かれている関数は step の外で呼び出す

Good:

```typescript
await navigateToMain(page);

await test.step("ダウンロードボタンをクリックしてモーダルを表示", async () => {
  await page.getByRole("button", { name: "ダウンロード" }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
});

await test.step("モーダル内の規約リンクが正しいか確認", async () => {
  await expect(page.getByRole("link", { name: "利用規約" })).toHaveAttribute(
    "href",
    "/term/",
  );
});
```

Bad:

```typescript
await navigateToMain(page);
await page.getByRole("button", { name: "ダウンロード" }).click();
await expect(page.getByRole("dialog")).toBeVisible();
```

## 共通化

### locator・変数の共有

locator の宣言場所は使用範囲で決める:

- **複数 step で使う**: test 関数直下で宣言
- **1つの step でのみ使う**: その step 内で宣言（外に出さない）

Good:

```typescript
test("テスト名", async ({ page }) => {
  const input = page.getByLabel("入力欄");

  await test.step("入力", async () => {
    await input.fill("テスト");
  });

  await test.step("検証", async () => {
    const accentPhrase = page.locator(".accent-phrase");
    await expect(input).toHaveValue("テスト");
    await expect(accentPhrase).toBeVisible();
  });
});
```

Bad 1 (不要な外部宣言):

```typescript
test("テスト名", async ({ page }) => {
  const accentPhrase = page.locator(".accent-phrase");

  await test.step("検証", async () => {
    await expect(accentPhrase).toBeVisible();
  });
});
```

Bad 2 (重複宣言):

```typescript
test("テスト名", async ({ page }) => {
  await test.step("入力", async () => {
    const input = page.getByLabel("入力欄");
    await input.fill("テスト");
  });

  await test.step("検証", async () => {
    const input = page.getByLabel("入力欄");
    await expect(input).toHaveValue("テスト");
  });
});
```

### ロジックの共通化

| スコープ              | 方法                                  |
| --------------------- | ------------------------------------- |
| test 内のみ           | test 関数内で変数やローカル関数を定義 |
| ファイル内の複数 test | ファイルスコープでローカル関数を定義  |
| 複数ファイル          | 共通ファイルにエクスポート関数を追加  |

## 既存コードとの整合

既存ファイル・関数名の指定がある場合はそれを優先。ない場合は既存 E2E の命名・スタイルに合わせる。
