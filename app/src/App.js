import React from "react";
import { CookiesProvider, withCookies } from "react-cookie";
import { Route, Routes } from "react-router-dom";
import { Activation, ResendActivation} from './pages/Activation';

function App() {
  return (
    <div className="App">
      <CookiesProvider>
        <Routes>
          <Route>
            <Route path="/activate/:uid/:token" element={<Activation />} />
            <Route path="/resendactivation" element={<ResendActivation />} />
          </Route>
        </Routes>
      </CookiesProvider>
    </div>
  );
}

export default withCookies(App);
