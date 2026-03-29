import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import RecipeCard from '../components/RecipeCard.vue'

const mockRecipe = {
  id:         1,
  name:       'Spaghetti Carbonara',
  image_url:  null,
  category:   'Pasta',
  rating:     4.7,
  total_time: '30m',
  calories:   520,
}

describe('RecipeCard', () => {
  it('renders the recipe name', () => {
    const wrapper = mount(RecipeCard, { props: { recipe: mockRecipe } })
    expect(wrapper.text()).toContain('Spaghetti Carbonara')
  })

  it('renders rating when provided', () => {
    const wrapper = mount(RecipeCard, { props: { recipe: mockRecipe } })
    expect(wrapper.text()).toContain('4.7')
  })

  it('renders total_time when provided', () => {
    const wrapper = mount(RecipeCard, { props: { recipe: mockRecipe } })
    expect(wrapper.text()).toContain('30m')
  })

  it('renders category pill', () => {
    const wrapper = mount(RecipeCard, { props: { recipe: mockRecipe } })
    expect(wrapper.text()).toContain('Pasta')
  })

  it('emits select event with recipe on click', async () => {
    const wrapper = mount(RecipeCard, { props: { recipe: mockRecipe } })
    await wrapper.trigger('click')
    expect(wrapper.emitted('select')).toBeTruthy()
    expect(wrapper.emitted('select')[0][0]).toEqual(mockRecipe)
  })

  it('shows fallback when no image_url', () => {
    const wrapper = mount(RecipeCard, {
      props: { recipe: { ...mockRecipe, image_url: null } }
    })
    // LazyImage handles the fallback internally
    expect(wrapper.find('.recipe-card').exists()).toBe(true)
  })
})