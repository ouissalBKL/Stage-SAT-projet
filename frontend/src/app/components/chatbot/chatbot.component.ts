import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { UserSessionService } from '../../services/user-session.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatbotService } from '../../services/chatbot.service';

interface Message {
  content: string;
  isUser: boolean;
  timestamp: Date;
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit, AfterViewInit {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  @ViewChild('questionInput') questionInput!: ElementRef;

  messages: Message[] = [];
  question: string = '';
  isLoading: boolean = false;
  showSpecialistModal: boolean = false;
  isSpecialist: boolean | null = null;
  userName: string = '';

  constructor(private chatbotService: ChatbotService, private userSession: UserSessionService) {}

  ngOnInit() {
    const user = this.userSession.getUser();
    if (user) {
      this.userName = (user.first_name && user.last_name) ? `${user.first_name} ${user.last_name}` : (user.first_name || user.last_name || '');
      this.isSpecialist = user.specialist ?? null;
  let welcomeMsg = `Bienvenue ${this.userName} ! Je suis votre assistant virtuel en gestion des approvisionnements, prêt à vous accompagner.`;
      this.messages.push({
        content: welcomeMsg,
        isUser: false,
        timestamp: new Date()
      });
      if (this.isSpecialist === true) {
        this.messages.push({
          content: "Puisque vous êtes spécialiste, je vais vous donner des réponses adaptées à votre niveau d'expertise.",
          isUser: false,
          timestamp: new Date()
        });
      } else if (this.isSpecialist === false) {
        this.messages.push({
          content: "Puisque vous n'êtes pas spécialiste, je vais vous expliquer les concepts de façon claire et accessible.",
          isUser: false,
          timestamp: new Date()
        });
      }
    } else {
      this.messages.push({
        content: "Bienvenue ! Je suis votre assistant virtuel en gestion des approvisionnements, prêt à vous accompagner.",
        isUser: false,
        timestamp: new Date()
      });
    }
  }

  ngAfterViewInit() {
    this.scrollToBottom();
  }



  async askQuestion() {
    if (!this.question.trim()) return;
    

    // Supprimer le message de bienvenue s'il existe
    if (this.messages.length > 0 && this.messages[0].content.includes("Bienvenue")) {
      this.messages.shift();
    }

    // Ajouter le message de l'utilisateur
    this.messages.push({
      content: this.question,
      isUser: true,
      timestamp: new Date()
    });

    // Ajouter un message de chargement
    const loadingMessage: Message = {
      content: "Chargement...",
      isUser: false,
      timestamp: new Date()
    };
    this.messages.push(loadingMessage);
    this.scrollToBottom();

    this.isLoading = true;
    const userQuestion = this.question;
    this.question = '';

    try {
      const response = await this.chatbotService.askQuestion(userQuestion).toPromise();
      
      // Remplacer le message de chargement par la réponse
      this.messages[this.messages.length - 1] = {
        content: response.response || response.error || 'Erreur inconnue',
        isUser: false,
        timestamp: new Date()
      };
    } catch (error) {
      this.messages[this.messages.length - 1] = {
        content: "Erreur réseau.",
        isUser: false,
        timestamp: new Date()
      };
    } finally {
      this.isLoading = false;
      this.scrollToBottom();
    }
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.askQuestion();
    }
  }

  copyToClipboard(content: string) {
    navigator.clipboard.writeText(content).then(() => {
      // Optionnel: afficher un message de confirmation
    });
  }

  formatMessage(content: string): string {
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }

  private scrollToBottom() {
    setTimeout(() => {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
      }
    }, 100);
  }
}
