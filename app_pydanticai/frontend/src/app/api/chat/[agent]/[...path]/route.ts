import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

const API_BASE_URL = process.env.LLM_API_URL || 'http://dev_backend:8080';

// Ensure we're using the container-to-container URL
if (!API_BASE_URL.startsWith('http://dev_backend')) {
  throw new Error('Invalid API_BASE_URL configuration');
}

export async function POST(request: NextRequest) {
  try {
    // Get URL and parse segments
    const url = new URL(request.url);
    const segments = url.pathname.split('/');
    // /api/chat/[agent]/[...path] -> agent is at index 3, path starts at index 4
    const agent = segments[3];
    const pathSegments = segments.slice(4).join('/');

    // Clone headers and add necessary ones
    const headers = new Headers(request.headers);
    headers.set('Content-Type', 'application/json');
    headers.set('Accept', request.headers.get('Accept') || 'application/json');

    // Get request body
    const body = await request.json();
    
    // Construct backend URL
    const backendUrl = `${API_BASE_URL}/${agent}/${pathSegments}`;
    
    // Check if this is a streaming request
    const isStreamRequest = request.headers.get('Accept') === 'text/event-stream';

    if (isStreamRequest) {
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: Object.fromEntries(headers.entries()),
        body: JSON.stringify(body),
      });

      return new NextResponse(response.body, {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    } else {
      // Handle regular JSON response
      const response = await axios.post(backendUrl, body, {
        headers: Object.fromEntries(headers.entries()),
        timeout: 30000
      });

      return NextResponse.json(response.data, {
        status: response.status,
        headers: {
          'Content-Type': 'application/json',
        },
      });
    }
    
  } catch (error) {
    console.error('API proxy error:', error);
    
    if (axios.isAxiosError(error)) {
      return NextResponse.json(
        { 
          error: 'Backend API Error',
          message: error.message,
          status: error.response?.status || 500
        },
        { status: error.response?.status || 500 }
      );
    }
    
    return NextResponse.json(
      { 
        error: 'Internal Server Error',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
