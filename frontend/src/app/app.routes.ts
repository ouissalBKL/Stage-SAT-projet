import { Routes } from '@angular/router';
import { ChatbotComponent } from './components/chatbot/chatbot.component';
import { AuthentificationComponent } from './components/authentification/authentification.component';

export const routes: Routes = [
  { path: '', redirectTo: '/authentification', pathMatch: 'full' },
  { path: 'authentification', component: AuthentificationComponent },
  { path: 'chatbot', component: ChatbotComponent }
];
