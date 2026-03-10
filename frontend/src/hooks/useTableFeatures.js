import { useState } from 'react';

/**
 * A custom hook to handle generic searching and sorting for any data array.
 * @param {Array} data - The raw array of objects from the API.
 * @param {Array} searchFields - An array of string keys to search within (e.g., ['email', 'student_id']).
 */
export const useTableFeatures = (data, searchFields = []) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [sortConfig, setSortConfig] = useState({ key: 'id', direction: 'asc' });

    // Handle column header clicks
    const handleSort = (key) => {
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };

    // Return the correct arrow based on current sort state
    const renderSortArrow = (key) => {
        if (sortConfig.key !== key) return null;
        return sortConfig.direction === 'asc' ? ' ↑' : ' ↓';
    };

    // 1. Filter the data
    const filteredData = data.filter(item => {
        if (!searchTerm) return true; // If no search term, return all
        
        const searchLower = searchTerm.toLowerCase();
        // Check if ANY of the specified fields contain the search term
        return searchFields.some(field => {
            const value = item[field];
            return value && value.toString().toLowerCase().includes(searchLower);
        });
    });

    // 2. Sort the filtered data
    const processedData = [...filteredData].sort((a, b) => {
        let valA = a[sortConfig.key];
        let valB = b[sortConfig.key];

        if (valA === null || valA === undefined) valA = '';
        if (valB === null || valB === undefined) valB = '';

        if (typeof valA === 'string' && typeof valB === 'string') {
            return sortConfig.direction === 'asc' 
                ? valA.localeCompare(valB) 
                : valB.localeCompare(valA);
        }

        if (valA < valB) return sortConfig.direction === 'asc' ? -1 : 1;
        if (valA > valB) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
    });

    return {
        searchTerm,
        setSearchTerm,
        handleSort,
        renderSortArrow,
        processedData // This is the final array to render in the table
    };
};