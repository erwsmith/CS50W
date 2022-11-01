import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Search from './Search';

const App = () => {
  return (
    <div className='container'>Search Results: <Search /></div>
  );
}

export default App;
