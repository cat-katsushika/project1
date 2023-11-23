import React from "react";
import { CookiesProvider, withCookies } from "react-cookie";
import { Route, Routes } from "react-router-dom";
import { Activation } from './pages/Activation';

function App() {
  return (
    <div className="App">
      <CookiesProvider>
        <Routes>
          <Route>
            <Route path="/activate/:uid/:token" element={<Activation />} />
            <Route path="/" />
          </Route>
        </Routes>
      </CookiesProvider>
    </div>
  );
}

export default withCookies(App);
