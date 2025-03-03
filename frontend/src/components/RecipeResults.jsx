import React from 'react';

function RecipeResults({ recipes }) {
    return (
        <div>
            <h2>Recipe Results:</h2>
            <ul>
                {recipes.map((recipe, index) => (
                    <li key={index}>
                        <a href={recipe.link} target="_blank" rel="noopener noreferrer">
                            {recipe.title}
                        </a>
                        <p>{recipe.snippet}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default RecipeResults;
