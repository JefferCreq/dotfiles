# Load chatcpp environment variables from config file
if test -f ~/.config/fish/.env
    source ~/.config/fish/.env
else
    echo "⚠️  Configuration file ~/.config/fish/.env not found"
    echo "Please create it with your API keys. See .env.example for reference"
end

function chatcpp
    # Verify that required environment variables are set
    if test -z "$AI_PROVIDER"
        echo "❌ AI_PROVIDER not set. Please configure ~/.config/fish/.chatcpp_env"
        return 1
    end
    
    # Check if the required API key for the provider is set
    switch $AI_PROVIDER
        case "openai"
            if test -z "$OPENAI_API_KEY"
                echo "❌ OPENAI_API_KEY not set for OpenAI provider"
                return 1
            end
        case "deepseek"
            if test -z "$DEEPSEEK_API_KEY"
                echo "❌ DEEPSEEK_API_KEY not set for DeepSeek provider"
                return 1
            end
        case "gemini"
            if test -z "$AI_API_KEY"
                echo "❌ AI_API_KEY not set for Gemini provider"
                return 1
            end
    end

    if test (count $argv) -eq 0
        echo "❌ Please provide a prompt. Example: chatcpp \"What is an API?\""
        return 1
    end

    set provider ""
    set args
    set next_is_provider 0

    for arg in $argv
        if test "$arg" = "--provider"
            set next_is_provider 1
            set args $args $arg
        else if test $next_is_provider -eq 1
            set provider $arg
            set next_is_provider 0
            set args $args $arg
        else
            set args $args $arg
        end
    end

    if test -z "$provider"
        set provider $AI_PROVIDER
    end

    set preprompt 'Your role is to act as an advanced English language assistant. I will provide you with a prompt, potentially written with grammatical errors or in a way that is not idiomatic for native English speakers. Your task is to:


First, **Correct my grammar and phrasing:**  Identify any errors in my original prompt and rewrite it to be grammatically correct and sound natural for a native English speaker. Clearly present the corrected prompt.
  

Then, **Answer the prompt:** After correcting and explaining, directly answer the corrected prompt as completely and accurately as possible, following its original intention.

Start by acknowledging my prompt and present the correction first inside triple backticks, then the answer.'

    set response (tgpt --preprompt "$preprompt" -q $args | grep -v "Loading" | string collect)

    echo "$response" | glow -p

    echo -e "\n🕘 "(date "+%Y-%m-%d %H:%M")"\n🌐 Provider: $provider\n📝 Prompt: $argv\n\n$response\n\n---" >> /data/.chatcpp_history.md
end

alias cpphist "env LESS='+G' glow -p /data/.chatcpp_history.md"

