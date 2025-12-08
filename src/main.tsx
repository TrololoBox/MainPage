import React from "react";
import ReactDOM from "react-dom/client";
import ProstoKitHome from "./ProstoKitHome";
import { FeatureFlagProvider } from "./featureFlags/FeatureFlagProvider";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <FeatureFlagProvider>
      <ProstoKitHome />
    </FeatureFlagProvider>
  </React.StrictMode>,
);
