# Classrooms React Key Runtime Fix

## Original Warning
React console reported a runtime warning on the `/classrooms` and `/datasets` page:
`Warning: Each child in a list should have a unique "key" prop.`
The application was using `key={c.Room_ID}` when mapping the classrooms array.

## Root Cause
An inspection of the actual data contract returned by the API (`GET /api/datasets/{dataset_size}/classrooms`) revealed that the unique identifier field from the dataset is actually named `Classroom_ID`, not `Room_ID`. Because `Room_ID` was `undefined`, React fell back to treating the key as invalid or duplicate across all items, triggering the unique key warning.

## Code Fix
1. **API Alignment**: Updated the rendering logic in `web/frontend/src/app/classrooms/page.tsx` and `web/frontend/src/app/datasets/page.tsx` to use the correct `Classroom_ID` property (e.g. `key={c.Classroom_ID}`).
2. **Type Safety Improvements**: Eliminated arbitrary `any` typing by defining the explicit `Classroom` and `Course` TypeScript interfaces mapping to the exact API JSON response structure.
3. **Data Casting**: Explicitly cast the `Capacity` property using `Number(c.Capacity)` to resolve TypeScript comparison errors during build (e.g., `TS2365: Operator '>' cannot be applied to types 'string | number' and 'number'.`) since the API returns capacity as a string representation of a number.

## Verification
- **Build Result**: SUCCESS. `npm run build` completed via Turbopack with 0 TypeErrors.
- **Browser Console**: SUCCESS. Headless browser verification confirmed the runtime execution throws 0 React key warnings and 0 hydration warnings.
- **UI Rendering**: Verified that classroom cards mount successfully, accurately displaying the `Classroom_ID`, capacity string, room types, and facility badges based on dynamic conditional rendering without duplicating or missing records.
