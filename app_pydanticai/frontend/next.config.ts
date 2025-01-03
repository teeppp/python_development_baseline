import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {
      enabled: true,
    },
  },
  serverComponentsExternalPackages: ["axios"],
};

export default nextConfig;
