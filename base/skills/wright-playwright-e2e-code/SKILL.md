---
name: wright-playwright-e2e-code
description: Playwright を用いた E2E テストコードを生成します。test.step を使った日本語ベースの実装スタイルに従い、コメント禁止の規約を守ります。E2E テスト、Playwright、テストコード生成が必要な場合に使用してください。
---

Playwright を用いた E2E テストの操作ロジックを記述してください。
以下の実装スタイルに厳密に従う必要があります。

## 最重要スタイルガイド：コメント禁止・日本語 Step 強制

テスト内の論理的な区切りは、コメントではなく `await test.step("日本語", async () => { ... })` で表現します。
「何をして、何を確認するか」がテストレポート上で読める日本語の step 名にします（体言止めよりも動作が分かる表現を優先）。
step は細かすぎず粗すぎず、ユーザー操作単位・UI 状態確認単位で区切ります。必要なら step の入れ子も使います。
アサーション（expect）も可能な限り、関連する `test.step` の内部に含めてください。

## 良い記述例（Good）

```typescript
await test.step("ダウンロードボタンをクリックしてモーダルを表示", async () => {
  const downloadButton = page.getByRole("button", { name: "ダウンロード" });
  await downloadButton.click();
  await expect(page.getByRole("dialog")).toBeVisible();
});

await test.step("モーダル内の規約リンクが正しいか確認", async () => {
  const link = page.getByRole("link", { name: "利用規約" });
  await expect(link).toHaveAttribute("href", "/term/");
});
```

## 悪い記述例（Bad）

```typescript
// ダウンロードボタンをクリック
await page.getByRole("button", { name: "ダウンロード" }).click();
// モーダルが表示されたか確認
await expect(page.getByRole("dialog")).toBeVisible();
```

既存ファイル・関数名の指定がある場合はそれを最優先し、ない場合は既存 E2E で使われている名前・流儀に合わせて実装する。
