import { NextResponse } from 'next/server';
import axios from 'axios';

const API_BASE_URL = 'http://dev_backend:8080';

export async function GET() {
  try {
    console.log('Fetching OpenAPI spec from:', `${API_BASE_URL}/openapi.json`);
    const response = await axios.get(`${API_BASE_URL}/openapi.json`, {
      timeout: 10000
    });

    return new NextResponse(JSON.stringify(response.data), {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('OpenAPI proxy error:', error);
    
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
