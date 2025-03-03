import React, { useState } from 'react';
import IngredientDetectionForm from './components/IngredientDetectionForm';
import RecipeSearchForm from './components/RecipeSearchForm';
import RecipeResults from './components/RecipeResults';
import './App.css';

function App() {
    const [ingredients, setIngredients] = useState([]);
    const [recipes, setRecipes] = useState([]);

    return (
        <div className="App">
            <h1>Precision Baking</h1>
            <IngredientDetectionForm setIngredients={setIngredients} />
            {ingredients.length > 0 && (
                <>
                    <h2>Detected Ingredients:</h2>
                    <ul>
                        {ingredients.map((item, index) => (
                            <li key={index}>{item.name} - {item.quantity}</li>
                        ))}
                    </ul>
                    <RecipeSearchForm ingredients={ingredients} setRecipes={setRecipes} />
                </>
            )}
            {recipes.length > 0 && <RecipeResults recipes={recipes} />}
        </div>
    );
}

export default App;

