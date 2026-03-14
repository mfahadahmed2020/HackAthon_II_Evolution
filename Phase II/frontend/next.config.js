/** @type {import('next').NextConfig} */
const nextConfig = {
  // API rewrites - proxy /api/* to backend
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  // Enable React strict mode for development
  reactStrictMode: true,
  // Output standalone for Docker deployment
  output: 'standalone',
}

module.exports = nextConfig
