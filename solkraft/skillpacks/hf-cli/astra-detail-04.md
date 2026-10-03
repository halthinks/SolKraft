### `hf collections` — Interact with collections on the Hub.

- `hf collections add-item COLLECTION_SLUG ITEM_ID ITEM_TYPE` — Add an item to a collection. `[--note TEXT --exists-ok --format [auto|human|agent|json|quiet]]`
- `hf collections create TITLE` — Create a new collection on the Hub. `[--namespace TEXT --description TEXT --private --exists-ok --format [auto|human|agent|json|quiet]]`
- `hf collections delete COLLECTION_SLUG` — Delete a collection from the Hub. `[--missing-ok --format [auto|human|agent|json|quiet]]`
- `hf collections delete-item COLLECTION_SLUG ITEM_OBJECT_ID` — Delete an item from a collection. `[--missing-ok --format [auto|human|agent|json|quiet]]`
- `hf collections info COLLECTION_SLUG` — Get info about a collection on the Hub. `[--format [auto|human|agent|json|quiet]]`
- `hf collections list` — List collections on the Hub. `[--owner TEXT --item TEXT --sort [lastModified|trending|upvotes] --limit INTEGER --format [auto|human|agent|json|quiet]]`
- `hf collections update COLLECTION_SLUG` — Update a collection's metadata on the Hub. `[--title TEXT --description TEXT --position INTEGER --private --theme TEXT --format [auto|human|agent|json|quiet]]`
- `hf collections update-item COLLECTION_SLUG ITEM_OBJECT_ID` — Update an item in a collection. `[--note TEXT --position INTEGER --format [auto|human|agent|json|quiet]]`
