import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

test("the development script uses the supported Webpack bundler", async () => {
  const packageJson = JSON.parse(
    await readFile(new URL("../package.json", import.meta.url), "utf8"),
  );

  assert.equal(packageJson.scripts.dev, "next dev --webpack");
});

test("the production build uses the supported Webpack bundler", async () => {
  const packageJson = JSON.parse(
    await readFile(new URL("../package.json", import.meta.url), "utf8"),
  );

  assert.equal(packageJson.scripts.build, "next build --webpack");
});
