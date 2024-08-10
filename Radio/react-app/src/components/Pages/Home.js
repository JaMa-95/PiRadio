import React from "react";
import { useState } from 'react';

import './Home.css';
import { RadioControl } from "./RadioControl/RadioControl";

export const Home = (props) => {
  return (
    <div class="main">
      <RadioControl />
    </div>
  );
};
