# React frontend

## Initial configuration

1. Upload your favicon in ./public
2. Upload your logo and icon in ./assets

## Code Splitting & Bundle Optimization

This project uses code-splitting to keep bundle sizes small and improve load times. Follow these practices when adding features:

### 1. Always Lazy Load New Routes

When adding a new page/route, use `React.lazy()`:

```typescript
// ✅ DO: Lazy load the page
const NewPage = lazy(() => import("@/pages/NewPage"));

// ❌ DON'T: Import statically
import NewPage from "@/pages/NewPage";
```

Then wrap it in Suspense:

```typescript
{
  path: "/new-page",
  element: (
    <Suspense fallback={<LoadingFallback />}>
      <NewPage />
    </Suspense>
  )
}
```

### 2. Lazy Load Heavy Components

For large components used conditionally (modals, complex forms, editors), lazy load them:

```typescript
const HeavyModal = lazy(() => import("@/components/HeavyModal"));

// Use with Suspense
{showModal && (
  <Suspense fallback={<div>Loading...</div>}>
    <HeavyModal />
  </Suspense>
)}
```

### 3. Update Manual Chunks for New Heavy Dependencies

When adding a new large library (>50KB), add it to `vite.config.ts`:

```typescript
manualChunks: {
  // Add new chunk for new heavy library
  'charts-vendor': ['recharts', 'chart.js'], // Example
}
```

**Common libraries to chunk separately:**

- Chart libraries (recharts, chart.js)
- Rich text editors (TipTap, Slate)
- PDF viewers
- Data table libraries (TanStack Table)
- Date pickers with locales

### 4. Keep Layouts Statically Imported

Layouts and core components should remain static imports since they're needed immediately:

```typescript
// ✅ Static import for layouts
import ProtectedLayout from "@/layouts/ProtectedLayout";
import LoadingFallback from "@/components/LoadingFallback";
```

### 5. Monitor Bundle Sizes

Check your build output regularly:

- Individual chunks should ideally be **< 200-300 KB**
- If a vendor chunk grows too large (>500KB), split it further
- Run `npm run build` to review the size report

### 6. Avoid Lazy Loading Small Components

Don't lazy load everything - there's overhead to code-splitting:

```typescript
// ❌ DON'T: Lazy load small utilities
const Button = lazy(() => import("@/components/Button"));

// ✅ DO: Keep small, frequently used components as static imports
import { Button } from "@/components/ui/button";
```

### Quick Checklist for New Features

- New route page? → Use `lazy()` + `Suspense`
- Heavy modal/dialog? → Consider lazy loading
- New large dependency (>50KB)? → Add to manual chunks
- Small reusable component? → Keep as static import
- After adding feature, run `npm run build` to check sizes
