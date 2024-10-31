import { render } from 'preact';
import { LocationProvider, Router, Route } from 'preact-iso';

import { Header } from './components/Header.jsx';
import { Home } from './pages/Home/Home.jsx';
import { Frequencies } from './pages/Frequencies/Frequencies.jsx';
import { Settings } from './pages/Settings/Settings.jsx';
import { Contact } from './pages/Contact/Contact.jsx';
import { NotFound } from './pages/_404.jsx';
import './style.css';

export function App() {
	return (
		<LocationProvider>
			<Header />
			<main>
				<Router>
					<Route path="/" component={Home} />
					<Route path="/frequencies" component={Frequencies} />
					<Route path="/settings" component={Settings} />
					<Route path="/contact" component={Contact} />
					<Route default component={NotFound} />
				</Router>
			</main>
		</LocationProvider>
	);
}

render(<App />, document.getElementById('app'));
