import axios from 'axios';

export const occurEarthQuake = async () => {
    const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/earthquakes/occur`);
    return response.data;
};
