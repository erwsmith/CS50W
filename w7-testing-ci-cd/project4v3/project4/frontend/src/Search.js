import React, { useState, useEffect }  from 'react';
import axios from 'axios';

const Search = () => {
    const [posts, setPosts] = useState([]);
    
    useEffect(() => {
        const search = async () => {
            const { data } = await axios.get('/api/posts/');
            console.log(data);
            setPosts(data);
        };
        search();
    }, []);

    const renderedPosts = posts.map((post) => {
        return (
            <div key={post.id}>
                <div className='container border'>
                    user: {post.user}, {post.body}, {post.timestamp}, liked by: {post.liked_by}
                </div>
            </div>
        )
    })

    return (
        <div>
            <div className='header'>{ renderedPosts }</div>
        </div>
    )
}

export default Search;