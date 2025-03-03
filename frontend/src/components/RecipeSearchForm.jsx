import React, { useState } from 'react';
import axios from 'axios';

function RecipeSearchForm({ ingredients, setRecipes }) {
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        setLoading(true);
        try {
            const ingredientNames = ingredients.map((item) => item.name);
            const response = await axios.post('http://127.0.0.1:5000/search_recipes', { ingredients: ingredientNames });
            setRecipes(response.data.recipes);
        } catch (error) {
            console.error('Error fetching recipes:', error);
        }
        setLoading(false);
    };

    return (
        <div>
            <button onClick={handleSearch} disabled={loading}>
                {loading ? 'Searching...' : 'Search Recipes'}
            </button>
        </div>
    );
}

export default RecipeSearchForm;


