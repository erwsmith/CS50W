import React, { useState, useEffect }  from 'react';
import axios from 'axios';

const Search = () => {
    const [posts, setPosts] = useState([]);
    
    useEffect(() => {
        const search = async () => {
            const { data } = await axios.get('http://127.0.0.1:8000/api/posts/');
            console.log(data[0]);
            setPosts(data);
        };
    }, []);

    return (
        <div>
            <h1 className='header'>{ posts }</h1>
        </div>
    )
}

export default Search;