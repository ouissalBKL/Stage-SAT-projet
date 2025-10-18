import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = 'http://localhost:8000/api/v1/endpoints';

  constructor(private http: HttpClient) {}

  // setSpecialist(isSpecialist: boolean): Observable<any> {
  //   const answer = isSpecialist ? 'oui' : 'non';
  //   return this.http.post(`${this.apiUrl}/set_specialist`, { answer });
  // }

  askQuestion(question: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/ask`, { question });
  }

  predictProduct(sku: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/predict/${sku}`);
  }

  predictAllProducts(): Observable<any> {
    return this.http.get(`${this.apiUrl}/predict/all`);
  }
}


