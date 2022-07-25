import VK_photoGetter
import YaDiscUpLoader


if __name__ == '__main__':
    vk_token = "vk1.a.ibVOqO5kiTOJAmzVN6iH6Hs35Ic26hGVHaMEXcNTAI-A63PdOJ5v3qnmx8-FP1_25mZR1Ny0URNICmyHCdSbLIeyWvxdAFzYaOl54yRGej4Z7mK-u7NlTueEpVK0d20-YR2eDh71Vt-J9XJ4Upg2GTAOonIYYNcUFJ1jvppg465nppPPrLSTS8z6dGpYhoFX"
    user_id = input("Input ID VK user")
    cnt_phts = input("Input the number of photos(default is 5): ")
    ya_token = input("Input ya_token: ")


    if not isinstance(cnt_phts, int):
        cnt_phts = 5

    VK = VK_photoGetter.VK_photoGetter(vk_token, user_id, cnt_phts)
    YD = YaDiscUpLoader.YaDiscUpLoader(ya_token, cnt_phts)

    response = VK.get_response()
    if response:
        YD.start_upload(response)
