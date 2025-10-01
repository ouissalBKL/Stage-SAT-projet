import { Component } from '@angular/core';
import { ChatbotComponent } from './chatbot/chatbot.component';

@Component({
  selector: 'app-root',
  imports: [ChatbotComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  title = 'Assistant Approvisionnement';
}
