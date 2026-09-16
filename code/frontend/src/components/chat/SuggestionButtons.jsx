import React from 'react';
import { SUGGESTION_PROMPTS } from '../../utils/constants';
import { Sparkles } from 'lucide-react';

export function SuggestionButtons({ onSelectSuggestion, suggestions = SUGGESTION_PROMPTS }) {
  return (
    <div className="flex flex-col gap-2 my-4">
      <div className="flex items-center gap-1.5 text-xs text-[#930500] font-semibold uppercase tracking-wider">
        <Sparkles className="w-3.5 h-3.5" /> Gợi ý câu hỏi phổ biến:
      </div>
      <div className="flex flex-wrap gap-2">
        {suggestions.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => onSelectSuggestion(prompt)}
            className="px-4 py-2 rounded-full bg-[#FFF8E7] hover:bg-[#95BBEA] text-[#2B2523] hover:text-[#1F242B] border border-[#EFE7D3] hover:border-[#95BBEA] text-xs font-medium transition-all duration-300 shadow-diffused-sm text-left hover:scale-[1.02] active:scale-95 cursor-pointer"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
