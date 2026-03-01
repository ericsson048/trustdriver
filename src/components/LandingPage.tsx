import React, { useState } from 'react';
import { ArrowRight, HardDrive, Shield, Share2, Zap } from 'lucide-react';

interface LandingPageProps {
  onGetStarted: () => void;
  onLogin: () => void;
}

export default function LandingPage({ onGetStarted, onLogin }: LandingPageProps) {
  return (
    <div className="min-h-screen bg-white font-sans text-gray-900">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <HardDrive className="text-white w-5 h-5" />
          </div>
          <span className="text-xl font-bold tracking-tight">Trust Driver</span>
        </div>
        <div className="flex items-center space-x-4">
          <button 
            onClick={onLogin}
            className="text-gray-600 hover:text-gray-900 font-medium px-4 py-2"
          >
            Sign In
          </button>
          <button 
            onClick={onGetStarted}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-5 py-2.5 rounded-full transition-colors"
          >
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-6 py-20 md:py-32 max-w-7xl mx-auto text-center">
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
          Your files, anywhere. <br /> Secure and fast.
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
          Store, share, and collaborate on files and folders from any mobile device, tablet, or computer. The best place for all your files.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
          <button 
            onClick={onGetStarted}
            className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white text-lg font-semibold px-8 py-4 rounded-full transition-all transform hover:scale-105 shadow-lg shadow-blue-600/20 flex items-center justify-center space-x-2"
          >
            <span>Start for free</span>
            <ArrowRight className="w-5 h-5" />
          </button>
          <button 
            onClick={onLogin}
            className="w-full sm:w-auto bg-gray-100 hover:bg-gray-200 text-gray-900 text-lg font-semibold px-8 py-4 rounded-full transition-all"
          >
            Existing User?
          </button>
        </div>
      </section>

      {/* Features Grid */}
      <section className="px-6 py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto grid md:grid-cols-3 gap-12">
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
              <Shield className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold mb-3">Secure Storage</h3>
            <p className="text-gray-600">
              Your files are encrypted and stored securely. We prioritize your privacy and data security above all else.
            </p>
          </div>
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
            <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-6">
              <Share2 className="w-6 h-6 text-indigo-600" />
            </div>
            <h3 className="text-xl font-bold mb-3">Easy Sharing</h3>
            <p className="text-gray-600">
              Share files and folders with anyone using a simple link. Control access and manage permissions effortlessly.
            </p>
          </div>
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mb-6">
              <Zap className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold mb-3">Lightning Fast</h3>
            <p className="text-gray-600">
              Upload and download files at high speeds. Our infrastructure is optimized for performance.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-12 border-t border-gray-200">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <HardDrive className="text-gray-400 w-5 h-5" />
            <span className="font-semibold text-gray-500">Trust Driver</span>
          </div>
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Trust Driver. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
