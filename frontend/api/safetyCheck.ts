import axios from 'axios';

interface SafetyCheckResponse {
  user_id: string;
  timestamp: string;
  status: string;
  location: string;
}

export const safetyCheck = async (): Promise<SafetyCheckResponse[]> => {
  const response = await axios.get<SafetyCheckResponse[]>(`${process.env.NEXT_PUBLIC_API_URL}/safetyCheck`);
  return response.data;
};
