import React, { useState } from 'react';
import axios from 'axios';

function IngredientDetectionForm({ setIngredients }) {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:5000/detect', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setIngredients(response.data.ingredients);
        } catch (error) {
            console.error('Error detecting ingredients:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Upload an Image</h2>
            <input type="file" onChange={handleFileChange} required />
            <button type="submit">Detect Ingredients</button>
        </form>
    );
}

export default IngredientDetectionForm;

