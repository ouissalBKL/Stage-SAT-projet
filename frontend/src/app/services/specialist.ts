
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Specialist {

  private apiUrl = 'http://localhost:8000/api/v1/endpoints'; // URL de ton backend

  constructor(private http: HttpClient) { }

  setSpecialist(status: boolean): Observable<any> {
    return this.http.post(`${this.apiUrl}/set_specialist`, { answer: status ? 'oui' : 'non' });
  }

  // si besoin, une méthode pour récupérer le statut depuis le backend
  getSpecialist(): Observable<any> {
    return this.http.get(`${this.apiUrl}/get_specialist`);
  }
}
