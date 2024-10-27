import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';
import os from 'os';

function getLocalIpAddress() {
	const interfaces = os.networkInterfaces();
	for (const name of Object.keys(interfaces)) {
		for (const iface of interfaces[name]) {
			if (iface.family === 'IPv4' && !iface.internal) {
				return "http://" + iface.address + ":8000";
			}
		}
	}
	return 'http://127.0.0.1:8000';
}

function getLocalIpAddressWs() {
	const interfaces = os.networkInterfaces();
	for (const name of Object.keys(interfaces)) {
		for (const iface of interfaces[name]) {
			if (iface.family === 'IPv4' && !iface.internal) {
				return "ws://" + iface.address + ":8000";
			}
		}
	}
	return 'ws://127.0.0.1:8000';
}

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [preact()],
	server: {
		port: 3000,
		host: '0.0.0.0',
		proxy: {
			'/api': {
				target: getLocalIpAddress(), // Replace with your backend server URL
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, ''),
			},
			'/socket': {
				target: getLocalIpAddress(), // Replace with your backend server URL
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/socket/, ''),
			},
		},
	},
});