import { useLocation } from 'preact-iso';

export function Header() {
	const { url } = useLocation();

	return (
		<header>
			<nav>
				<a href="/" class={url == '/' && 'active'}>
					Home
				</a>
				<a href="/frequencies" class={url == '/frequencies' && 'active'}>
					Frequencies
				</a>
				<a href="/settings" class={url == '/settings' && 'active'}>
					Settings
				</a>
				<a href="/Contact" class={url == '/Contact' && 'active'}>
					Contact
				</a>
			</nav>
		</header>
	);
}
