import React from 'react';

function FAQPage() {
  const faqs = [
    {
      question: "What is included in the tour package?",
      answer: "Most tours include transportation, a guide, and some admission fees. Check each tour's details."
    },
    {
      question: "Can I get a refund if I cancel?",
      answer: "Cancellation policies vary per tour. Contact support for details."
    },
    {
      question: "Do you offer group discounts?",
      answer: "Yes, for groups above a certain size. Contact us via WhatsApp or email for more info."
    }
  ];

  return (
    <div className="faq-page">
      <h2>Frequently Asked Questions</h2>
      {faqs.map((faq, idx) => (
        <div key={idx} className="faq-item">
          <p className="question">{faq.question}</p>
          <p className="answer">{faq.answer}</p>
        </div>
      ))}
    </div>
  );
}

export default FAQPage;
