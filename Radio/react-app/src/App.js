import "./App.css";
import NavBar from "./components/NavBar";
import { BrowserRouter as Router,  Route, Routes } from "react-router-dom";
import { Home } from "./components/Pages/Home";
import { Settings } from "./components/Pages/Settings";
import { Frequencies } from "./components/Pages/Frequencies";
import { Contact } from "./components/Pages/Contact";

function App() {
  return (
    <>
      <Router>
        <NavBar />
        <div className="pages">
          <Routes>
            <Route path="/" element={<Home className="page"/>} />
            <Route path="/frequencies" element={<Frequencies />} />
            <Route path="/settings" element={<Settings className="page"/>} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </div>
      </Router>
  </>
  );
}

export default App;