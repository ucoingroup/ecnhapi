import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const data = JSON.parse(await readFile(new URL("../data/api-ecosystem.json", import.meta.url), "utf8"));
const requiredKeys = [
  "name",
  "icon",
  "category",
  "type",
  "fit",
  "free",
  "freeLimit",
  "startingPrice",
  "note",
  "ecnhValue",
  "useCases",
];

assert.equal(data.apis.filter((api) => api.category === "social").length, 10, "must include 10 social APIs");
assert.equal(data.apis.filter((api) => api.category === "ai").length, 10, "must include 10 AI APIs");
assert.ok(data.apis.filter((api) => api.free).length >= 8, "must include at least 8 APIs with free tiers");
assert.ok(data.apis.filter((api) => api.fit === "best").length >= 6, "must include at least 6 best-fit APIs");
assert.equal(new Set(data.apis.map((api) => api.name)).size, data.apis.length, "API names must be unique");

for (const api of data.apis) {
  for (const key of requiredKeys) {
    assert.ok(Object.hasOwn(api, key), `${api.name} missing ${key}`);
  }
  assert.match(api.category, /^(social|ai)$/);
  assert.match(api.fit, /^(best|good|low)$/);
  assert.ok(Array.isArray(api.useCases) && api.useCases.length >= 3, `${api.name} needs use cases`);
}

assert.ok(Array.isArray(data.stack) && data.stack.length === 3, "must define three eCNH stack layers");
console.log("API ecosystem data is valid.");
