import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar/Navbar";

export const metadata: Metadata = {
  title: "StoicBite - Get your daily dose of stoicism!",
  description: "Get your daily dose of stoicism!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="relative">
        <Navbar /> {children}
      </body>
    </html>
  );
}
