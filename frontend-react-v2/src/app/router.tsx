import { lazy, Suspense, type ComponentType } from 'react'
import { createBrowserRouter } from 'react-router-dom'
import { AppShell } from './layout'
import { RequireAuth } from './guards'
import { InitPage } from '@/features/init/InitPage'
import { LoginApiPage } from '@/features/auth/LoginPage'
import { RegisterPage } from '@/features/auth/RegisterPage'
import { ManagementPage } from '@/features/management/ManagementPage'
import { ResourcePage } from '@/features/management/ResourcePage'
import { DetailPage } from '@/features/lookup/DetailPage'
import { HomePage, LogoutPage, NotFoundPage } from './pages'
import { AnalysisWorkspacePage } from '@/features/analysis/AnalysisWorkspacePage'
const StatisticsPage = lazy(() =>
  import('@/features/analysis/AnalysisChartPage').then((module) => ({
    default: module.StatisticsPage,
  })),
)
const ComparisonPage = lazy(() =>
  import('@/features/analysis/ComparisonPage').then((module) => ({
    default: module.ComparisonPage,
  })),
)

const LookupPageV2 = lazy(() =>
  import('@/features/lookup/LookupPage').then((module) => ({ default: module.LookupPageV2 })),
)
const LazyLookup = (
  <Suspense fallback={<section className="dense-card status-panel">Loading Lookup...</section>}>
    <LookupPageV2 />
  </Suspense>
)

export const router = createBrowserRouter([
  { path: '/login', element: <LoginApiPage /> },
  { path: '/register', element: <RegisterPage /> },
  { path: '/logout', element: <LogoutPage /> },
  {
    element: <RequireAuth />,
    children: [
      {
        element: <AppShell />,
        children: [
          { path: '/', element: <HomePage /> },
          { path: '/initialization', element: <InitPage /> },
          { path: '/lookup', element: LazyLookup },
          { path: '/detail', element: <DetailPage /> },
          { path: '/management', element: <ManagementPage /> },
          { path: '/project', element: <ResourcePage kind="project" /> },
          { path: '/logformat', element: <ResourcePage kind="logformat" /> },
          { path: '/metrics', element: <ResourcePage kind="metrics" /> },
          { path: '/analysis', element: <AnalysisWorkspacePage /> },
          { path: '/statistics', element: <LazyAnalysis component={StatisticsPage} /> },
          { path: '/comparison_chart', element: <LazyAnalysis component={ComparisonPage} /> },
          { path: '/comparison_statistic', element: <LazyAnalysis component={StatisticsPage} /> },
        ],
      },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
])

function LazyAnalysis({ component: Component }: { component: ComponentType }) {
  return (
    <Suspense fallback={<section className="dense-card status-panel">Loading charts...</section>}>
      <Component />
    </Suspense>
  )
}
