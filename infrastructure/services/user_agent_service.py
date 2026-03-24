from user_agents import parse

class UserAgentService:
    
    @staticmethod
    def parse_user_agent(user_agent_string: str) -> dict:
        if not user_agent_string:
            return {
                "device_type": None,
                "os": None,
                "browser": None
            }
        
        try:
            user_agent = parse(user_agent_string)
            
            if user_agent.is_mobile:
                device_type = "Mobile"
            elif user_agent.is_tablet:
                device_type = "Tablet"
            elif user_agent.is_pc:
                device_type = "Desktop"
            elif user_agent.is_bot:
                device_type = "Bot"
            else:
                device_type = "Unknown"
            
            # Sistema operacional
            os_name = f"{user_agent.os.family}"
            if user_agent.os.version_string:
                os_name += f" {user_agent.os.version_string}"
            
            # Navegador
            browser_name = f"{user_agent.browser.family}"
            if user_agent.browser.version_string:
                browser_name += f" {user_agent.browser.version_string}"
            
            return {
                "device_type": device_type,
                "os": os_name if os_name != "Other" else None,
                "browser": browser_name if browser_name != "Other" else None
            }
        except Exception as e:
            print(f"Erro ao parsear User Agent: {e}")
            return {
                "device_type": None,
                "os": None,
                "browser": None
            }
