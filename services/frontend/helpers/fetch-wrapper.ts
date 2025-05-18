import { useAuthStore } from '~/stores/auth.store';
import type { RequestOptions, MyHeaders } from '~/types';

export const fetchWrapper = {
    get: request('GET'),
    post: request('POST'),
    put: request('PUT'),
    delete: request('DELETE')
}

function request(method: string) {
    return (url: string, body?: any, { credentials }: RequestOptions = {}) => {
        if (url.startsWith('/')) {
            const meta= import.meta.env.VITE_API_URL === undefined?'https://emprender-radix.com/api' : import.meta.env.VITE_API_URL;
            url = `${meta}${url}`;
        }
        const requestOptions: RequestInit = {
            method,
            headers: authHeader(url) as MyHeaders
        };

        if (body) {
            if (isFormData(body)) {
                // If the body is an instance of FormData, do not set Content-Type, 
                // the browser will set it automatically including the boundary.
                requestOptions.body = body;
            } else {
                const headers = requestOptions.headers as MyHeaders;
                headers["Content-Type"] = "application/json";
                requestOptions.body = JSON.stringify(body);
            }
        }
        if (credentials) {
            requestOptions.credentials = credentials;
        }
        return fetch(url, requestOptions).then(handleResponse);
    }
}

function isFormData(value: any): value is FormData {
    return value instanceof FormData;
}

// Helper Functions
function authHeader(url: string): HeadersInit {
    // Return auth header with jwt if user is logged in and request is to the api url
    const { user } = useAuthStore();
    const isLoggedIn: boolean = !!user?.access;
    
    const meta= import.meta.env.VITE_API_URL === undefined?'https://emprender-radix.com/api' : import.meta.env.VITE_API_URL;
    const isApiUrl = url.startsWith(meta);
    if (isLoggedIn && isApiUrl) {
        return { Authorization: `Bearer ${user?.access}` };
    }
    return {};
}

async function handleResponse(response: Response): Promise<any> {
    const text = await response.text();
    const data = text && JSON.parse(text);
    if (!response.ok) {
        //const { user, logout } = useAuthStore();
        /*if ([401, 403].includes(response.status) && user) {
            // auto logout if 401 Unauthorized or 403 Forbidden response returned from api                
            await logout();
        }*/
        const error = (data || data.message) || response.statusText;
        throw error;
    }
    return data;
}
