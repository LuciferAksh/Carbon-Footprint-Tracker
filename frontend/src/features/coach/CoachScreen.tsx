/**
 * @fileoverview AI Carbon Coach Chat screen.
 * Interactive chat assistant powered by Gemini 2.5 Flash,
 * and an interactive Eco-Quiz to educate users about carbon reduction.
 */
import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import {
  Send,
  MessageSquare,
  Sparkles,
  AlertCircle,
  RefreshCw,
  Trophy,
  CheckCircle2,
  XCircle,
  HelpCircle,
  ArrowRight,
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { api } from '@/lib/api';
import { Card, Skeleton } from '@/components/ui';
import Button from '@/components/ui/Button';

const QUIZ_LENGTH = 5;

interface Message {
  role: 'user' | 'model';
  content: string;
}

interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
}

const QUICK_PROMPTS = [
  'How do I lower my food footprint?',
  'Give me daily green travel tips',
  'Suggest a low-carbon shopping swap',
];

const QUIZ_QUESTIONS: QuizQuestion[] = [
  {
    id: 1,
    question: 'Which of the following diets has the lowest average carbon footprint?',
    options: [
      'Vegetarian diet with dairy',
      'Fully vegan diet',
      'Poultry and fish-based diet',
      'High-protein meat diet',
    ],
    correctAnswer: 1,
    explanation:
      'A fully vegan diet has the lowest carbon footprint, saving up to 60-70% of food emissions compared to a diet high in red meat.',
  },
  {
    id: 2,
    question:
      'How much energy/CO₂ does a typical LED bulb save compared to an old incandescent bulb?',
    options: ['About 10% to 20%', 'About 30% to 50%', 'About 75% to 80%', 'Over 95%'],
    correctAnswer: 2,
    explanation:
      'LED bulbs use up to 80% less electricity than traditional incandescent bulbs, drastically reducing grid power demand and carbon emissions.',
  },
  {
    id: 3,
    question:
      'For a 10 km daily commute, which transport mode has the highest emissions per passenger-kilometer?',
    options: ['Bus', 'Electric Vehicle (EV)', 'Single-occupant petrol car', 'Metro/Subway train'],
    correctAnswer: 2,
    explanation:
      'A single-occupant petrol car emits roughly 0.21 kg CO₂ per km, whereas a metro emits less than 0.04 kg per passenger-kilometer.',
  },
  {
    id: 4,
    question: 'What does the term "Phantom energy drain" refer to?',
    options: [
      'Energy used by electric vehicles while parked',
      'Electricity consumed by devices plugged in on standby mode',
      'Solar energy lost due to cloudy weather',
      'Heat leaking through poorly insulated windows',
    ],
    correctAnswer: 1,
    explanation:
      'Phantom energy (or standby load) is the power drawn by appliances like TVs, chargers, and microwaves while they are plugged in but turned off. It accounts for up to 10% of household bills.',
  },
  {
    id: 5,
    question: 'Which action has the highest single impact on reducing household carbon emissions?',
    options: [
      'Recycling all household plastic bottles',
      'Switching to a 100% renewable energy tariff or solar panels',
      'Turning off lights when leaving a room',
      'Reusing grocery bags',
    ],
    correctAnswer: 1,
    explanation:
      'Switching your energy supply to renewable grid tariffs or installing home solar panels can reduce your annual household carbon footprint by 1 to 2 tonnes, far exceeding the impact of standard recycling.',
  },
];

/**
 * AI Carbon Coach interactive chat and Eco-Quiz component.
 */
export default function CoachScreen() {
  const [activeTab, setActiveTab] = useState<'chat' | 'quiz'>('chat');

  // --- Chat State ---
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'model',
      content:
        "Hello! I'm your CarbonCoach. Ask me anything about your carbon footprint, suggestions to reduce it, or ways to hit your weekly challenges! How can I help you today?",
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // --- Quiz State ---
  const [quizStarted, setQuizStarted] = useState(false);
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [quizLoading, setQuizLoading] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [quizScore, setQuizScore] = useState(0);
  const [quizFinished, setQuizFinished] = useState(false);

  const scrollToBottom = useCallback(() => {
    if (typeof messagesEndRef.current?.scrollIntoView === 'function') {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  useEffect(() => {
    if (activeTab === 'chat') {
      scrollToBottom();
    }
  }, [messages, loading, activeTab, scrollToBottom]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMessage: Message = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);
    setError(null);

    try {
      const history = [...messages, userMessage];
      const response = await api.post<{ reply: string }>('/insights/chat', {
        messages: history.map((msg) => ({
          role: msg.role,
          content: msg.content,
        })),
      });

      setMessages((prev) => [...prev, { role: 'model', content: response.data.reply }]);
    } catch {
      setError('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSendMessage(inputValue);
  };

  // --- Quiz Actions ---
  const startQuiz = async () => {
    setQuizStarted(true);
    setQuizLoading(true);
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setSelectedOption(null);
    setIsAnswered(false);
    setQuizScore(0);
    setQuizFinished(false);

    try {
      const response = await api.get<QuizQuestion[]>('/insights/quiz?count=5');
      if (response && response.data && response.data.length > 0) {
        setQuestions(response.data);
      } else {
        throw new Error('Invalid API response');
      }
    } catch (err) {
      console.error('Failed to fetch dynamic questions, using fallback', err);
      setQuestions(QUIZ_QUESTIONS);
    } finally {
      setQuizLoading(false);
    }
  };

  const handleOptionSelect = (optionIndex: number) => {
    if (isAnswered || !questions[currentQuestionIndex]) return;
    setSelectedOption(optionIndex);
    setIsAnswered(true);

    if (optionIndex === questions[currentQuestionIndex].correctAnswer) {
      setQuizScore((prev) => prev + 1);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setSelectedOption(null);
      setIsAnswered(false);
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      setQuizFinished(true);
    }
  };

  const currentQuestion = questions[currentQuestionIndex];

  const quizFeedbackMessage = useMemo(() => {
    const percentage = (quizScore / QUIZ_LENGTH) * 100;
    if (percentage === 100)
      return {
        title: '🌍 Climate Hero!',
        desc: 'Perfect score! You have master-level carbon footprint knowledge!',
      };
    if (percentage >= 80)
      return {
        title: '🌱 Eco Warrior!',
        desc: 'Great job! You have a solid grasp on how to reduce emissions.',
      };
    if (percentage >= 60)
      return {
        title: '🍃 Green Apprentice!',
        desc: 'Good start! Try exploring the AI Coach chat tips to learn more.',
      };
    return {
      title: '🍂 Climate Novice',
      desc: 'Every step counts. Ask the AI Coach to explain tips to get better!',
    };
  }, [quizScore]);

  return (
    <main
      id="main-content"
      className="flex flex-col h-[calc(100dvh-4rem)] max-w-lg mx-auto px-4 pt-4 pb-20 relative"
      role="main"
    >
      {/* Tab Segment Controls */}
      <div className="flex bg-dark-900/80 p-1 rounded-xl mb-4 border border-dark-800/80 z-10">
        <button
          onClick={() => setActiveTab('chat')}
          className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
            activeTab === 'chat'
              ? 'bg-primary-600 text-white shadow shadow-primary-600/10'
              : 'text-dark-400 hover:text-white'
          }`}
          type="button"
          aria-pressed={activeTab === 'chat'}
        >
          Chat with Coach
        </button>
        <button
          onClick={() => setActiveTab('quiz')}
          className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
            activeTab === 'quiz'
              ? 'bg-primary-600 text-white shadow shadow-primary-600/10'
              : 'text-dark-400 hover:text-white'
          }`}
          type="button"
          aria-pressed={activeTab === 'quiz'}
        >
          Play Eco-Quiz
        </button>
      </div>

      <AnimatePresence mode="wait">
        {activeTab === 'chat' ? (
          <motion.div
            key="chat-tab"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 10 }}
            className="flex-1 flex flex-col min-h-0"
          >
            {/* Header */}
            <header className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-xl bg-primary-600/10 border border-primary-600/20 flex items-center justify-center text-primary-400">
                  <MessageSquare className="w-5 h-5" aria-hidden="true" />
                </div>
                <div>
                  <h1 className="text-sm font-bold text-white flex items-center gap-1.5">
                    CarbonCoach AI{' '}
                    <Sparkles className="w-4 h-4 text-primary-400" aria-hidden="true" />
                  </h1>
                  <p className="text-[10px] text-green-400 font-medium">Online & Ready</p>
                </div>
              </div>
            </header>

            {/* Messages viewport */}
            <div
              ref={chatContainerRef}
              className="flex-1 overflow-y-auto space-y-4 mb-4 pr-1 scrollbar-thin"
              aria-live="polite"
              aria-relevant="additions"
            >
              <AnimatePresence initial={false}>
                {messages.map((msg, index) => {
                  const isUser = msg.role === 'user';
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 15 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                          isUser
                            ? 'bg-primary-600 text-white rounded-br-none shadow-md shadow-primary-600/10'
                            : 'glass text-dark-100 rounded-bl-none border-dark-700/50'
                        }`}
                      >
                        <p>{msg.content}</p>
                      </div>
                    </motion.div>
                  );
                })}

                {/* Typing Indicator */}
                {loading && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="glass rounded-2xl rounded-bl-none px-4 py-3.5 flex items-center gap-1.5 border-dark-700/50">
                      <span
                        className="w-2 h-2 bg-primary-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0ms' }}
                      />
                      <span
                        className="w-2 h-2 bg-primary-400 rounded-full animate-bounce"
                        style={{ animationDelay: '150ms' }}
                      />
                      <span
                        className="w-2 h-2 bg-primary-400 rounded-full animate-bounce"
                        style={{ animationDelay: '300ms' }}
                      />
                    </div>
                  </motion.div>
                )}

                {/* Error Alert */}
                {error && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex justify-center"
                  >
                    <Card className="p-3 bg-red-950/20 border-red-800/30 text-red-400 text-xs flex items-center gap-2">
                      <AlertCircle className="w-4 h-4 flex-shrink-0" />
                      <span>{error}</span>
                      <button
                        onClick={() =>
                          handleSendMessage(messages[messages.length - 1]?.content || '')
                        }
                        className="p-1 hover:bg-dark-800 rounded text-red-300 transition-colors cursor-pointer"
                        aria-label="Retry sending last message"
                      >
                        <RefreshCw className="w-3.5 h-3.5" />
                      </button>
                    </Card>
                  </motion.div>
                )}
              </AnimatePresence>
              <div ref={messagesEndRef} />
            </div>

            {/* Quick suggestions */}
            {messages.length === 1 && !loading && (
              <div className="mb-4">
                <p className="text-[10px] text-dark-400 mb-2 font-medium uppercase tracking-wider">
                  Suggested Queries:
                </p>
                <div className="flex flex-wrap gap-2">
                  {QUICK_PROMPTS.map((prompt) => (
                    <button
                      key={prompt}
                      onClick={() => handleSendMessage(prompt)}
                      className="text-xs px-3 py-2 rounded-xl bg-dark-800/60 border border-dark-700 hover:border-primary-500 hover:bg-dark-800 text-dark-200 hover:text-white transition-all cursor-pointer focus-visible:outline-2 focus-visible:outline-primary-500"
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input panel */}
            <form onSubmit={handleSubmit} className="flex gap-2 relative z-10">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask CarbonCoach..."
                className="flex-1 bg-dark-900 border border-dark-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-primary-500 placeholder-dark-500"
                aria-label="Message input for AI Carbon Coach"
                disabled={loading}
              />
              <Button
                type="submit"
                disabled={!inputValue.trim() || loading}
                aria-label="Send message"
                className="w-12 h-12 flex items-center justify-center p-0 rounded-xl"
              >
                <Send className="w-4 h-4" />
              </Button>
            </form>
          </motion.div>
        ) : (
          <motion.div
            key="quiz-tab"
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            className="flex-1 flex flex-col min-h-0 justify-center items-center"
          >
            {!quizStarted ? (
              <Card className="p-6 text-center max-w-sm w-full border-primary-500/20">
                <div className="w-16 h-16 rounded-2xl bg-primary-600/10 border border-primary-600/20 flex items-center justify-center text-primary-400 mx-auto mb-4 animate-pulse">
                  <Trophy className="w-8 h-8" aria-hidden="true" />
                </div>
                <h1 className="text-xl font-bold text-white mb-2">Eco-Quiz Challenge</h1>
                <p className="text-sm text-dark-400 leading-relaxed mb-6">
                  Test your carbon knowledge! Play this interactive quiz to discover how you can
                  work to reduce your carbon footprint and save the environment. 🌍
                </p>
                <Button onClick={startQuiz} fullWidth size="lg">
                  Play Now
                </Button>
              </Card>
            ) : quizFinished ? (
              <Card className="p-6 text-center max-w-sm w-full border-primary-500/20">
                <div className="w-16 h-16 rounded-2xl bg-primary-600/20 border border-primary-600/30 flex items-center justify-center text-primary-400 mx-auto mb-4">
                  <Trophy className="w-8 h-8" />
                </div>
                <h2 className="text-xl font-bold text-white mb-1">{quizFeedbackMessage.title}</h2>
                <p className="text-xs text-primary-400 font-semibold mb-4">
                  You scored {quizScore} out of {QUIZ_LENGTH}
                </p>
                <p className="text-sm text-dark-400 mb-6 leading-relaxed">
                  {quizFeedbackMessage.desc}
                </p>
                <div className="space-y-3">
                  <Button onClick={startQuiz} fullWidth>
                    Play Again
                  </Button>
                  <Button onClick={() => setActiveTab('chat')} variant="secondary" fullWidth>
                    Ask Coach a Question
                  </Button>
                </div>
              </Card>
            ) : quizLoading ? (
              <div className="w-full max-w-md space-y-4">
                <div className="flex justify-between items-center text-xs text-dark-400 mb-1">
                  <Skeleton className="h-4 w-32" />
                  <Skeleton className="h-4 w-16" />
                </div>
                <div className="w-full h-1.5 bg-dark-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary-500 rounded-full transition-all duration-300"
                    style={{ width: `${((currentQuestionIndex + 1) / QUIZ_LENGTH) * 100}%` }}
                  />
                </div>
                <Card className="p-5 border-dark-800 space-y-4">
                  <Skeleton className="h-6 w-full" />
                  <Skeleton className="h-6 w-3/4" />

                  <div className="space-y-2.5 pt-4">
                    <Skeleton className="h-12 w-full rounded-xl" />
                    <Skeleton className="h-12 w-full rounded-xl" />
                    <Skeleton className="h-12 w-full rounded-xl" />
                    <Skeleton className="h-12 w-full rounded-xl" />
                  </div>
                </Card>
              </div>
            ) : currentQuestion ? (
              <div className="w-full max-w-md space-y-4">
                {/* Progress bar */}
                <div className="flex justify-between items-center text-xs text-dark-400 mb-1">
                  <span>
                    Question {currentQuestionIndex + 1} of {questions.length}
                  </span>
                  <span className="font-semibold text-primary-400">Score: {quizScore}</span>
                </div>
                <div className="w-full h-1.5 bg-dark-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary-500 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
                  />
                </div>

                <AnimatePresence mode="wait">
                  <motion.div
                    key={currentQuestionIndex}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.25 }}
                    className="space-y-4"
                  >
                    {/* Question Card */}
                    <Card className="p-6 border-dark-700/60 bg-dark-900/40 backdrop-blur-md shadow-xl shadow-black/10">
                      <h3 className="text-base font-semibold text-white mb-4 leading-relaxed flex gap-2">
                        <span className="text-primary-400 mt-0.5" aria-hidden="true">
                          <HelpCircle className="w-5 h-5 flex-shrink-0" />
                        </span>
                        {currentQuestion.question}
                      </h3>

                      {/* Options */}
                      <div className="space-y-2.5">
                        {currentQuestion.options.map((option, idx) => {
                          const isCorrect = idx === currentQuestion.correctAnswer;
                          const isSelected = idx === selectedOption;

                          let optionStyle =
                            'border-dark-700 hover:border-primary-500/50 hover:bg-dark-800/40';
                          let icon = null;

                          if (isAnswered) {
                            if (isCorrect) {
                              optionStyle =
                                'border-green-500 bg-green-950/30 text-green-300 font-medium shadow-md shadow-green-950/20';
                              icon = (
                                <CheckCircle2 className="w-4.5 h-4.5 text-green-400 flex-shrink-0" />
                              );
                            } else if (isSelected) {
                              optionStyle =
                                'border-red-500 bg-red-950/30 text-red-300 shadow-md shadow-red-950/20';
                              icon = <XCircle className="w-4.5 h-4.5 text-red-400 flex-shrink-0" />;
                            } else {
                              optionStyle = 'border-dark-800/50 opacity-40';
                            }
                          }

                          return (
                            <motion.button
                              key={idx}
                              onClick={() => handleOptionSelect(idx)}
                              disabled={isAnswered}
                              whileHover={isAnswered ? {} : { scale: 1.01, x: 2 }}
                              whileTap={isAnswered ? {} : { scale: 0.99 }}
                              className={`w-full flex items-center justify-between text-left p-3.5 rounded-xl border text-sm transition-all focus:outline-none focus:ring-1 focus:ring-primary-500 ${
                                !isAnswered ? 'cursor-pointer' : 'cursor-default'
                              } ${optionStyle}`}
                              type="button"
                            >
                              <span>{option}</span>
                              {icon}
                            </motion.button>
                          );
                        })}
                      </div>
                    </Card>

                    {/* Explanation Card */}
                    {isAnswered && (
                      <motion.div
                        initial={{ opacity: 0, y: 15 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-4"
                      >
                        <Card className="p-4.5 bg-primary-950/20 border-primary-800/30 shadow-lg backdrop-blur-md">
                          <h4 className="text-xs font-semibold text-primary-400 mb-1.5 flex items-center gap-1.5">
                            <Sparkles className="w-3.5 h-3.5 text-primary-400" /> CarbonCoach
                            Insight
                          </h4>
                          <p className="text-xs text-dark-200 leading-relaxed">
                            {currentQuestion.explanation}
                          </p>
                        </Card>

                        <Button
                          onClick={handleNextQuestion}
                          fullWidth
                          icon={<ArrowRight className="w-4 h-4 animate-pulse" />}
                          className="shadow-lg shadow-primary-600/15"
                        >
                          {currentQuestionIndex === questions.length - 1
                            ? 'Finish Quiz'
                            : 'Next Question'}
                        </Button>
                      </motion.div>
                    )}
                  </motion.div>
                </AnimatePresence>
              </div>
            ) : null}
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
