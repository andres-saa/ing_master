import axios from "axios";
import { URI } from "../conection";

export const restaurantService = {
    // Obtener todos los restaurantes disponibles
    async getAllRestaurants() {
        try {
            const response = await axios.get(`${URI}/restaurants`);
            if (response.status === 200) {
                return response.data;  // Devolver la lista de restaurantes
            } else {
                console.error('Error al obtener los restaurantes:', response.status);
                return [];
            }
        } catch (error) {
            console.error('Error al obtener los restaurantes:', error);
            return [];
        }
    }
};