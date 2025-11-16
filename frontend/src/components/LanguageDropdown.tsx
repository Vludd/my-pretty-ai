import { ChevronDown } from "lucide-react";
import { Button } from "./ui/button";

import { 
  DropdownMenu, 
  DropdownMenuContent,
  DropdownMenuRadioGroup, 
  DropdownMenuRadioItem, 
  DropdownMenuTrigger 
} from "./ui/dropdown-menu";

import { useState } from "react";

interface LanguageDropdownProps {
  languages: string[]
}

export default function LanguageDropdown({languages}: LanguageDropdownProps) {
  const defaultLang = languages.length > 0 ? languages[0] : "English"
  const [lang, setLang] = useState<string>(defaultLang)

  function handleLangSelect(selectedLang: string) {
    setLang(selectedLang)
  }

  return (
    <div>
      {languages.length > 1 ? (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline">
              <p>{lang}</p>
              <ChevronDown className="ml-auto" />
            </Button>
          </DropdownMenuTrigger>

          <DropdownMenuContent align="end">
              <DropdownMenuRadioGroup
                value={lang}
                onValueChange={handleLangSelect}
              >
                {languages.map(lang => (
                  <DropdownMenuRadioItem key={lang} value={lang}>
                    {lang}
                  </DropdownMenuRadioItem>
                ))}
              </DropdownMenuRadioGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      ) : (
        <div className="text-sm text-muted-foreground">
          {defaultLang}
        </div>
      )}
    </div>
  );
}